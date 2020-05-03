# cs4485-workshop-scheduler

## System Requirements

- [Python 3.7+ ](https://www.python.org/downloads/)
- [Google OR-Tools](https://developers.google.com/optimization/install)

## Running

Execute `main.py` with Python 3.7+.

## Testing Requirements

- Bash (or equivalent)
- Netcat (or equivalent)

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

### Webapp

The webapp makes heavy use of the framework Vue and several related
technologies. The following are some useful references we'd recommend for
general questions.

- [The official Vue.js docs](https://vuejs.org/v2/guide/) are the best source for
  information on vue and its different pieces. We provide links to specific sections
  of interest below as needed.
- We recommend installing the extension
  [Vue.js Devtools](https://github.com/vuejs/vue-devtools#installation) to help
  with browser debugging.
- [Mozilla Developer Network](https://developer.mozilla.org/en-US/) is a good
  source of documentation for web technologies.

#### General structure

There are 3 main pages to the web app:

- The Home Page: A simple landing page with links to the other two pages
- The Schedules Page: A (currently unimplemented) page for retrieving generated
  schedules from the server and visualizing them on a calendar
- The Constraints Page: Allows the user to input a list of
  constraints for theworkshop, with different categories and their
  appropriate properties. The rest of this documentation will be focused on this page.
  ![The Constraint Page](https://github.com/leapwill/cs4485-workshop-scheduler/raw/master/webapp/constraintpage.png)
