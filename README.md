# My Persistent Notifications

A custom sensor for Home Assistant that counts the number of active [persistent notifications](https://www.home-assistant.io/integrations/persistent_notification/), with optional filtering based on notification ID prefixes.

---

## 🔍 Purpose

This integration provides a simple sensor that:

- Shows the **total number of active persistent notifications** as the sensor state.
- Exposes all active notifications as a JSON list in the `notifications` attribute.
- Optionally adds extra attributes for **counts per ID prefix**, configured via YAML.

Useful for organizing and reacting to notifications from specific sources like `"cat"`, `"doorbell"`, `"update"`, etc.

---

## ✅ Example Functionality

Imagine you have 5 active notifications:

| ID         | Message             |
|------------|---------------------|
| `cat1`     | Feed Felix the cat        |
| `doorbell1`| Someone rang the bell |
| `cat2`     | Felix has entered the house    |
| `cat3`     | Felix has left the house        |
| `updates`  | Some message        |

With the following configuration:

```yaml
sensor:
  - platform: my_persistent_notifications
    filters:
      - cat
      - doorbell
```

The sensor will output:

```yaml
sensor.active_persistent_notifications:
  state: 5
  attributes:
    cat: 3
    doorbell: 1
    notifications:
      - id: cat1
        title: ...
        message: ...
      - ...
```

---

## ⚙️ Installation

1. 📁 Place the component inside your `custom_components` directory:

```
config/
└── custom_components/
    └── my_persistent_notifications/
        ├── __init__.py
        ├── sensor.py
        ├── manifest.json
        └── const.py (optional, currently unused)
```

2. 📄 Add to your `configuration.yaml`:

```yaml
sensor:
  - platform: my_persistent_notifications
    filters:
      - cat
      - doorbell
```

- `filters` is optional. Leave it out if you don’t need filtered counts.
- Notification IDs are set using the `notification_id` parameter in automations or scripts.

3. 🔁 Restart Home Assistant.

---

## 📊 Sensor Output

| Property         | Description                                                   |
|------------------|---------------------------------------------------------------|
| `state`          | Total number of active persistent notifications               |
| `notifications`  | A list of all active notifications (in JSON format)           |
| `cat`, `doorbell` (etc.) | Number of notifications with IDs starting with that prefix |

---

## 🧪 Tips

- You can create a notification with a specific ID in automations or scripts like this:

```yaml
service: persistent_notification.create
data:
  message: The cat wants food
  title: Cat Alert
  notification_id: cat3
```

- Use **Developer Tools → States** to inspect sensor output.
- Combine with automations for powerful notification-aware workflows.


---

## 📎 License

Free to use and modify. This is a community-driven project. 😄
