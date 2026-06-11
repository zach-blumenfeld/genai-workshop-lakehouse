# Participant run-through — exact steps

## 1. Open the course
http://localhost:3000/courses/genai-workshop-lakehouse/ — enroll, start Module 1,
follow every page in order. (After the PR merges this becomes
graphacademy.neo4j.com/courses/genai-workshop-lakehouse/ — same pages.)
If it shows "Coming Soon": flip `:status:` to `active` in course.adoc locally.

## 2. Lesson "Your Environment" — do what it says
- Click **Open in GitHub Codespace** → real cloud terminal, everything preinstalled (build takes a few minutes)
- THE ONE SUBSTITUTION: where the page shows database credentials, instead create a
  free **Graph Data Science blank sandbox** at https://sandbox.neo4j.com and paste
  THOSE credentials into `.env` (your local DB is unreachable from a cloud Codespace;
  in production GA provisions this sandbox for the participant)
- Continue exactly as the page says: `python load/load_graph.py`, then
  `uvicorn api.parts_api:app --port 8800` in a second terminal
  (404s for `/` or favicon in its log are normal - the API only serves /orders; leave it running.
  401 "x-api-key" when hitting it from a browser is also normal: scripts/agent send the key
  from .env automatically; for manual /docs testing the key is autofix-workshop-key)
- `claude` in a third terminal (one-time sign-in) and run the smoke-test question
  (if `claude: command not found`: `npm install -g @anthropic-ai/claude-code`;
  if `neo4j-cli` missing: `curl -sSfL https://neo4j.sh/install.sh | bash && export PATH="$HOME/.local/bin:$PATH"`)

## 2b. REQUIRED after creating your sandbox — repoint the Check Database buttons
The local course's verify buttons check your LOCAL db, but your work lives in the
cloud sandbox. Fix (once): edit `~/dev/courses/docker-compose.override.yaml` and
replace the four SANDBOX_DEV_INSTANCE_* lines under `app:` with your sandbox values:

```yaml
      SANDBOX_DEV_INSTANCE_HOST: <sandbox IP, no scheme>
      SANDBOX_DEV_INSTANCE_PORT: <bolt port>
      SANDBOX_DEV_INSTANCE_USERNAME: neo4j
      SANDBOX_DEV_INSTANCE_PASSWORD: <sandbox password>
```

Then: `cd ~/dev/courses && docker compose up -d app` and hard-refresh the course page.
Now Check Database buttons (and the embedded sandbox pane) hit the same database
your Codespace writes to.

## 3. Modules 2-5 — no substitutions
Follow the lesson pages exactly: fill the blanks (M2, M3), build from spec (M4),
hand the events to Claude, click the Check Database buttons, take the quiz.

## Restart clean (full reset, no partial fixes)
1. Delete the Codespace: https://github.com/codespaces → ... menu on it → Delete
2. Wipe the cloud sandbox (or just keep it - the load script is safe to re-run):
   from any terminal with its creds: `MATCH (n) DETACH DELETE n`
3. Re-enter at step 1 (the course page) and click the Codespace button again -
   the setup script is fixed, so a fresh Codespace builds complete

## If stuck
`solutions/scripts/` in the Codespace has every completed script.
