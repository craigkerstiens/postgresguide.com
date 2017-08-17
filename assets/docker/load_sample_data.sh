#~/bin/bash

createdb pgguide
pg_restore --no-owner --dbname pgguide /tmp/example.dump