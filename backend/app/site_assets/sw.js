// Shows the bot's push notifications for the home-screen app. No caching: the app always loads fresh data.
self.addEventListener("install", () => self.skipWaiting());
self.addEventListener("activate", event => event.waitUntil(self.clients.claim()));

self.addEventListener("push", event => {
  let data = {};
  try { data = event.data ? event.data.json() : {}; } catch (e) { data = { body: event.data ? event.data.text() : "" }; }
  event.waitUntil(self.registration.showNotification(data.title || "Min depå", {
    body: data.body || "", icon: "icon-192.png", badge: "icon-192.png", data: { url: data.url || "./" },
  }));
});

self.addEventListener("notificationclick", event => {
  event.notification.close();
  event.waitUntil(self.clients.matchAll({ type: "window", includeUncontrolled: true }).then(wins => {
    for (const w of wins) if ("focus" in w) return w.focus();
    return self.clients.openWindow(event.notification.data && event.notification.data.url || "./");
  }));
});
