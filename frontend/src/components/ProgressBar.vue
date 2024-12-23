<script lang="ts">
  export default {
    props: {
      progress: {
        type: Number,
        required: true,
      },
    },
  };
</script>

<template>
  <div class="w-full bg-gray-200 rounded-full h-4 mb-4">
    <div
      class="bg-green-500 h-4 rounded-full"
      :style="{ width: progress + '%' }"
    ></div>
    <p class="text-center text-sm text-gray-600">
      進度: {{ progress.toFixed(2) }}%
    </p>
  </div>
</template>
