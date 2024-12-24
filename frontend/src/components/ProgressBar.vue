<script lang="ts">
  import PrimeProgressBar from "primevue/progressbar";

  export default {
    name: "CustomProgressBar",
    components: {
      PrimeProgressBar,
    },
    props: {
      progress: {
        type: Number,
        required: true,
      },
    },
  };
</script>

<template>
  <PrimeProgressBar :value="Number(progress.toFixed(2))" />
</template>
