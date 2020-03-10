let app = new Vue({
    el: '#app',
    data: {
        message: "Hello World!",
        app1Visible: true
    },
    methods: {
        selectConstraints: function () {
            constraintComponent.constraintsVisible = true;
            app.app1Visible = false;
        },
        selectSchedule: function () {
            scheduleComponent.scheduleVisible = true;
            app.app1Visible = false;
        },
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
        submitCsv: function (e) {
            e.preventDefault();
            const file = document.querySelector('form#form-csv input[type="file"]').files[0];
            const reader = new FileReader();
            const xhr = new XMLHttpRequest();
            const statusEl = document.querySelector('form#form-csv div.form-status');
            xhr.upload.addEventListener('load', () => {
                statusEl.classList.add('success');
                statusEl.textContent = 'CSV upload succeeded';
            });
            xhr.upload.addEventListener('error', (e) => {
                statusEl.classList.add('error');
                statusEl.textContent = 'CSV upload failed: ' + e.message;
                console.error(e);
            });
            xhr.open('POST', 'post_csv');
            xhr.overrideMimeType('text/csv');
            reader.addEventListener('load', (e) => {
                xhr.send(e.target.result);
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