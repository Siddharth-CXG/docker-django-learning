# Data Model: Energy Dashboard

## ContactMessage

Represents a visitor's submitted contact form. This is the only persisted feature entity.

| Field | Type | Required | Rules |
|---|---|---:|---|
| `id` | Auto-increment integer | Yes | Primary key managed by Django |
| `name` | Short text | Yes | Trim whitespace; maximum 100 characters |
| `email` | Email text | Yes | Must pass Django email validation; maximum 254 characters |
| `message` | Text | Yes | Trim whitespace; non-empty |
| `created_at` | Date/time | Yes | Set automatically when the record is created |

### Lifecycle and validation

1. The visitor submits name, email, and message.
2. The standard Django form rejects missing/whitespace-only values, malformed email, and values over field limits; invalid input is re-rendered with field errors and entered values.
3. A valid form creates one SQLite record, then displays a success confirmation. No email is sent.
4. The record remains in the SQLite database for local review. It is not exposed through a public list page because this feature has no authentication.

### Persistence

SQLite stores the database at `/app/data/db.sqlite3` in the container. A named Docker volume mounted at `/app/data` preserves it across container replacement. The initial schema is managed through Django migrations.

## EnergyAsset

The four asset examples are fixed presentation data rather than database entities. Each contains a display name, one of the example types (Solar PV, Wind, Battery Storage), and a display status. No identity, lifecycle, or persistence behavior is required.

## Dashboard statistics

Total Assets, Active Assets, and Alerts are illustrative placeholders for the initial feature, not persisted aggregates. The sample values may be Total Assets 4, Active Assets 3, and Alerts 1, matching the four example assets.