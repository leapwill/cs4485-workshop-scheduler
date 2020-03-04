let app = new Vue({
    el: '#app',
    data: {
        message: "Hello World!",
        app1Visable:true
    },
    methods: {
        selectConstraints: function(){
            constraintComponent.constraintsVisable = true;
            app.app1Visable = false;
        },
        selectSchedule: function(){
            scheduleComponent.scheduleVisable = true;
            app.app1Visable = false;
        },
    }
})

let constraintComponent = new Vue({
    el: '#constraints',
    data: {
        constraintsVisable: false
    }
})

let scheduleComponent = new Vue({
    el: '#schedule',
    data: {
        scheduleVisable: false
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