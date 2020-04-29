# cs4485-workshop-scheduler

## System Requirements
 - [Python 3.7+ ](https://www.python.org/downloads/)
 - [Google OR-Tools](https://developers.google.com/optimization/install)

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
