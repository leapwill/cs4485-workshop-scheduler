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
});

let constraintComponent = new Vue({
    // TODO: fetch existing constraints from server and fill in
    el: '#constraints-app',
    data: {
        constraintsVisible: false,
        constraints2: {
            'instructors': [
                {
                    id: 1000, name: 'Ray Lewis', instruments: [
                        { name: 'Violin', canTeach: true, bookLevels: [2, 3, 4] },
                        { name: 'Viola', canTeach: true, bookLevels: [6, 7] },
                        { name: 'Cello', canTeach: false, bookLevels: [] },
                        { name: 'Piano', canTeach: false, bookLevels: [] }
                    ],
                    availableSlots: [1, 2, 3, 4, 5], maxSlots: 5
                },
                {
                    id: 1001, name: 'Catherine Adkins', instruments: [
                        { name: 'Violin', canTeach: false, bookLevels: [] },
                        { name: 'Viola', canTeach: false, bookLevels: [] },
                        { name: 'Cello', canTeach: true, bookLevels: [1, 2, 3, 4, 5] },
                        { name: 'Piano', canTeach: false, bookLevels: [] }
                    ],
                    availableSlots: [3, 4, 5], maxSlots: 2
                },
            ],
            'classtypes': [
                { type: 'Master Class', instruments: [], count: 0 },
                { type: 'Workshop', instruments: [], count: 0 },
                { type: 'Chamber Orchestra', count: 0 },
                { type: 'Elective Art', count: 0 },
                { type: 'Elective Composition', count: 0 }
            ],
            'rooms': [10, 5, 2] /* small, medium, large */
        },
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
            classes: { name: '', id: 2000, isRequired: false, isBookBased: false, bookLevelMin: 1, bookLevelMax: 3, isAgeBased: false, ageMin: 7, ageMax: 10, isInstrumentBased: false, instruments: [], roomSize: 0, enrollmentMax: 10, needsAccompanist: false }
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
            classes: []
        }
    },
    methods: {
        addEntry: function (e, type) {
            let newItem = {};
            newItem = Object.assign(newItem, this.defaults[type])
            if (this.constraints3[type].length !== 0) {
                let nextId = this.constraints3[type][this.constraints3[type].length - 1].id + 1;
                newItem.id = nextId;
            }
            this.constraints3[type].push(newItem);
        },
        deleteEntry: function (e, type, id) {
            for (i = 0; i < this.constraints3[type].length; i++) {
                if (this.constraints3[type][i].id === id) {
                    this.constraints3[type].splice(i, 1);
                    break;
                }
            }
        },
        submitCsv: function (e) {
            e.preventDefault();
            const file = document.querySelector('form#form-csv input[type="file"]').files[0];
            const reader = new FileReader();
            const xhr = new XMLHttpRequest();
            const statusEl = document.querySelector('form#form-csv div.form-status');
            xhr.addEventListener('load', () => {
                // TODO: refactor to fetch() and use setFormStatus()
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
    }
});

let scheduleComponent = new Vue({
    el: '#schedule',
    data: {
        scheduleVisible: false
    }
});
