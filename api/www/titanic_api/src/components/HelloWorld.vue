<template>
  <v-container>
    <v-layout
      text-xs-center
      wrap
    >
      <v-flex>
        <!-- IMPORTANT PART! --><form>
          <v-text-field
            v-model="pclass"
            label="Ticket Class"
            required
          ></v-text-field>
          <v-text-field
            v-model="name"
            label="Name"
            required
          ></v-text-field>
          <v-text-field
            v-model="sex"
            label="Sex"
            required
          ></v-text-field>
          <v-text-field
            v-model="age"
            label="Age"
            required
          ></v-text-field>
          <v-text-field
            v-model="sibsp"
            label="Siblings-Spouse"
            required
          ></v-text-field>
          <v-text-field
            v-model="parch"
            label="Parents-Children"
            required
          ></v-text-field>
          <v-text-field
            v-model="fare"
            label="Fare"
            required
          ></v-text-field>
          <v-text-field
            v-model="cabin"
            label="Cabin"
            required
          ></v-text-field>
          <v-text-field
            v-model="embarked"
            label="Embarked"
            required
          ></v-text-field>
          
          <v-btn @click="submit">submit</v-btn>
          <v-btn @click="clear">clear</v-btn>
        </form>
        <br/>
        <br/>
        <h1 v-if="predictedClass">Predicted Class is: {{ predictedClass }}</h1>
        <!-- END: IMPORTANT PART! -->
      </v-flex>
    </v-layout>
  </v-container>
</template>

<script>
  import axios from 'axios'
  export default {
    name: 'HelloWorld',
    data: () => ({
      pclass: '',
      name: '',
      sex: '',
      age: '',
      sibsp: '',
      parch:  '',
      fare: '',
      cabin: '',
      embarked: '',
      predictedClass : ''
    }),
    methods: {
    submit () {
      axios.post('http://127.0.0.1:5000/predict', {
        pclass: this.pclass,
        name: this.name,
        sex: this.sex,
        age: this.age,
        sibsp: this.sibsp,
        parch: this.parch,
        fare: this.fare,
        cabin: this.cabin,
        embarked: this.embarked
      })
      .then((response) => {
        this.predictedClass = response.data.class
      })
    },
    clear () {
        this.pclass = '',
        this.name = '',
        this.sex = '',
        this.age = '',
        this.sibsp = '',
        this.parch = '',
        this.fare = '',
        this.cabin = '',
        this.embarked = ''
    }
  }
}
</script>