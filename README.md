# cs4485-workshop-scheduler

## System Requirements
 - [Python 3.7+ ](https://www.python.org/downloads/)
 - [Google OR-Tools](https://developers.google.com/optimization/install)

## Running

Execute `main.py` with Python 3.7+.

## Testing Requirements
 * Bash (or equivalent)
 * Netcat (or equivalent)

## Testing
After running the server, to test with the default hostname and port of
`127.0.0.1:8080` do
```bash
bash test_requests.sh
```

or to provide a different hostname and port to use, do:
```bash
bash test_requests.sh [hostname] [port]
```

## Developer Notes

- This application is designed to be run locally and used by 1 user. We made a web front-end for convenience, it is not indented to be hosted like a typical website.
- Use [Vue.js Devtools](https://github.com/vuejs/vue-devtools#installation) to help with browser debugging.
- [MDN](https://developer.mozilla.org/en-US/) is a good source of documentation for web technologies.
