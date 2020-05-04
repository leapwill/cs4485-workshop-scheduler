Vue.component('back-button', {
    data: function () {
        return {
            goBack: function () {
                constraintComponent.constraintsVisible = false;
                scheduleComponent.scheduleVisible = false;
                window.location.hash = '';
                app.app1Visible = true;
            }
        }
    },
    template: '<div><button v-on:click="goBack()">← Back</button></div>'
});

let app = new Vue({
    el: '#app',
    data: {
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
});

let constraintComponent = new Vue({
    el: '#constraints-app',
    data: {
        constraintsVisible: false,
        loadConstraintsPromise: null,
        defaults: {
            instructors: {
                id: 9999, name: '', instruments: [
                    { name: 'Violin', canTeach: false, bookLevels: [] },
                    { name: 'Viola', canTeach: false, bookLevels: [] },
                    { name: 'Cello', canTeach: false, bookLevels: [] },
                    { name: 'Piano', canTeach: false, bookLevels: [] }
                ],
                availableSlots: [], maxSlots: 0
            },
            classes: { name: '', id: 2000, isRequired: false, isBookBased: false, bookLevelMin: 1, bookLevelMax: 3, isAgeBased: false, ageMin: 7, ageMax: 10, isInstrumentBased: false, instruments: [], roomSize: 0, enrollmentMax: 10, needsAccompanist: false },
            instructors: { name: '', id: 3000, instruments: [], classes: [], slotsAvailable: [], slotsMax: 5 }
        },
        constraints3: {
            workshop_instruments: [
                { name: 'Piano', isEnabled: false, bookLevelMin: 1, bookLevelMax: 10 },
                { name: 'Harp', isEnabled: false, bookLevelMin: 1, bookLevelMax: 10 },
                { name: 'Accompanist Piano', isEnabled: false, bookLevelMin: 1, bookLevelMax: 10 },
                { name: 'Violin', isEnabled: false, bookLevelMin: 1, bookLevelMax: 10 },
                { name: 'Viola', isEnabled: false, bookLevelMin: 1, bookLevelMax: 10 },
                { name: 'Cello', isEnabled: false, bookLevelMin: 1, bookLevelMax: 10 }
            ],
            workshop_schedule_slots: 5,
            classes: [],
            instructors: [],
            'rooms': [10, 5, 2] /* small, medium, large */
        }
    },
    methods: {
        addEntry: function (e, type) {
            let newItem = JSON.parse(JSON.stringify(this.defaults[type])); // deep copy without lodash
            if (this.constraints3[type].length !== 0) {
                let nextId = this.constraints3[type][this.constraints3[type].length - 1].id + 1;
                newItem.id = nextId;
            }
            this.constraints3[type].push(newItem);
        },
        deleteEntry: function (e, type, id) {
            // TODO: find and delete references (like instructor classes)
            if (confirm('Are you sure you want to delete this?')) {
                for (i = 0; i < this.constraints3[type].length; i++) {
                    if (this.constraints3[type][i].id === id) {
                        this.constraints3[type].splice(i, 1);
                        break;
                    }
                }
            }
        },
        instructorClassChanged: function (e, instructor, id) {
            let classes = instructor.classes;
            if (e.target.checked === true) {
                classes.push({ id: id });
            }
            else {
                let clsToRemove = classes.find(cls => cls.id === id);
                classes.splice(classes.indexOf(clsToRemove), 1);
            }
        },
        submitCsv: function (e) {
            e.preventDefault();
            if (confirm('Are you sure you want to upload new student data and reset the workshop?')) {
                const file = document.querySelector('form#form-csv input[type="file"]').files[0];
                const reader = new FileReader();
                // using ugly old syntax because FileReader is old and doesn't use Promises
                reader.addEventListener('load', (e) => {
                    fetch('post_csv', {
                        method: 'POST',
                        headers: { 'Content-Type': 'text/csv', 'Content-Encoding': 'base64' },
                        body: btoa(e.target.result)
                    }).then(response => {
                        const statusEl = document.querySelector('form#form-csv div.form-status')
                        this.setFormStatus(statusEl, response);
                    })
                });
                reader.readAsBinaryString(file);
            }
        },
        submitConstraints: async function () {
            let response = await fetch('post_constraints', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(this.constraints3)
            });
            let statusEl = document.querySelector('#btn-constraints + div.form-status');
            this.setFormStatus(statusEl, response);
        },
        setFormStatus(statusEl, response) {
            if (Math.floor(response.status / 100) === 2) {
                statusEl.classList.add('success');
                statusEl.textContent = 'Submit succeeded';
            }
            else {
                statusEl.classList.add('error');
                statusEl.textContent = 'Submit failed: ' + response.statusText;
                console.error(response);
            }
        }
    },
    created: function () {
        this.loadConstraintsPromise = fetch('/previous.json');
    },
    mounted: function () {
        this.loadConstraintsPromise.then(response => {
            if (Math.floor(response.status / 100) === 2) {
                response.json().then(json => this.constraints3 = json);
            }
        });
    }
});

let scheduleComponent = new Vue({
    el: '#schedule-app',
    data: {
        scheduleVisible: false
    }
});
