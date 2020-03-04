let app = new Vue({
    el: '#app',
    data: {
        message: "Hello World!",
        app1Visible:true
    },
    methods: {
        selectConstraints: function(){
            constraintComponent.constraintsVisible = true;
            app.app1Visible = false;
        },
        selectSchedule: function(){
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
    el: '#constraints',
    data: {
        constraintsVisible: false,
        //eventually the constraints will all be built and returned by reading
        //the list file
        constraints: [
            {id: 0, type:'times', value:'10-2'},
            {id: 1, type:'teachers', value:'Will'},
            {id: 2, type:'unique students', value: ['James','Michael']}
        ]
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