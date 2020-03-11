let app = new Vue({
    el: '#app',
    data: {
        message: "Hello World!",
        app1Visible: true
    },
    methods: {
        selectConstraints: function () {
            this.app1Visible = false;
            constraintComponent.constraintsVisible = true;
            window.location.hash = 'constraints';
        },
        selectSchedule: function () {
            this.app1Visible = false;
            scheduleComponent.scheduleVisible = true;
            window.location.hash = 'schedule';
        },
        restorePage: function () {
            // Restore correct page on reload or browser back/forward
            let hash = window.location.hash.substr(1);
            if (hash === 'constraints') {
                this.selectConstraints();
            }
            else if (hash === 'schedule') {
                this.selectSchedule();
            }
            else {
                constraintComponent.constraintsVisible = false;
                scheduleComponent.scheduleVisible = false;
                this.app1Visible = true;
            }
        }
    },
    mounted: function () {
        window.addEventListener('hashchange', this.restorePage);
        window.addEventListener('load', this.restorePage);
    }
})

Vue.component('constraintitem', {
    props: ['constraint'],
    template:
        `<div>{{constraint.type}} : {{constraint.value}}</div>`
})

let constraintComponent = new Vue({
    // TODO: fetch existing constraints from server and fill in
    el: '#constraints',
    data: {
        constraintsVisible: false,
        //eventually the constraints will all be built and returned by reading
        //the list file
        constraints: [
            { id: 0, type: 'times', value: '10-2' },
            { id: 1, type: 'teachers', value: 'Will' },
            { id: 2, type: 'unique students', value: ['James', 'Michael'] }
        ],
        constraints2: {
            'instructors': [
                { id: 1000, 'name': 'Ray Lewis', instruments: ['Violin', 'Viola'] },
                { id: 1001, 'name': 'Catherine Adkins', instruments: ['Cello'] }
            ],
            'rooms': [
                { id: 2000, 'number': 'NW 1204', capacity: 8 },
                { id: 2001, 'number': 'NE 1010', capacity: 40 }
            ]
        }
    },
    methods: {
        addRow: function (e) {
            // TODO: is there a better way to do this, like passing an arg from the v-on:click ?
            let category = e.target.parentElement.querySelector('strong').textContent.toLowerCase();
            let nextId = this.constraints2[category][this.constraints2[category].length - 1].id + 1;
            this.constraints2[category].push({ id: nextId, value: 'TODO' });
        },
        submitCsv: function (e) {
            e.preventDefault();
            const file = document.querySelector('form#form-csv input[type="file"]').files[0];
            const reader = new FileReader();
            const xhr = new XMLHttpRequest();
            const statusEl = document.querySelector('form#form-csv div.form-status');
            xhr.addEventListener('load', () => {
                if (Math.floor(xhr.status / 100) === 2) {
                    statusEl.classList.add('success');
                    statusEl.textContent = 'CSV upload succeeded';
                }
                else {
                    statusEl.classList.add('error');
                    statusEl.textContent = 'CSV upload failed: ' + xhr.statusText;
                    console.error(xhr);
                }
            });
            xhr.upload.addEventListener('error', (e) => {
                statusEl.classList.add('error');
                statusEl.textContent = 'CSV upload failed: ' + e.message;
                console.error(e);
            });
            xhr.open('POST', 'post_csv');
            xhr.overrideMimeType('text/plain');
            xhr.setRequestHeader('Content-Type', 'text/csv');
            xhr.setRequestHeader('Content-Encoding', 'base64');
            reader.addEventListener('load', (e) => {
                xhr.send(btoa(e.target.result));
            });
            reader.readAsBinaryString(file);
        }
    }
})

let scheduleComponent = new Vue({
    el: '#schedule',
    data: {
        scheduleVisible: false
    }
})


/*
NOTES

okaaay... so that's the extremely simple stuff put together. At the moment,
especially considering exactly what we're trying to build, I don't think a
single page-app is outside the realm of possibility.

Considering using a v-for (vue directive runs on each thing in a collection) to
render constraints in their own components. Will need to see how that works.
*/