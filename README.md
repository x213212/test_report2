# test_report2

The front end of a two-repository test-report application, packaged so the whole
stack comes up with one command.

The front end and back end live in separate repositories and separate
containers, joined by a shared Docker network — the split exists so either side
can be rebuilt and redeployed without touching the other. The companion
repository is [test_report](https://github.com/x213212/test_report).

## Stack

| Service | Role |
|---|---|
| app | the front end (Vue 3 + Element Plus) |
| `mongodb` | report storage |
| `redis` | cache and session store |
| `mynetwork` | shared bridge network the other half joins |

## Run

```bash
make up          # docker compose build && docker compose up -d
```

Then open <http://127.0.0.1/>.

```bash
make down        # stop and remove
make logs        # follow output
```

## Develop without Docker

```bash
npm install
npm run dev
```

## License

MIT. See [LICENSE](LICENSE).
