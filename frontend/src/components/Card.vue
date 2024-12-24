<script lang="ts">
  export default {
    props: {
      job: {
        type: Object,
        required: true,
      },
      index: {
        type: Number,
        required: true,
      },
    },
  };
</script>

<template>
  <div
    class="p-4 border border-gray-200 rounded-lg shadow-md hover:shadow-lg transition duration-300 ease-in-out"
  >
    <ul class="space-y-4 mt-4">
      <li>
        <h4 class="text-xl text-gray-900 mt-2">{{ job["Job Name"] }}</h4>
        <p class="text-gray-700 mt-2">
          公司名稱: <span>{{ job["Company Name"] }}</span>
        </p>
        <p class="text-gray-700">
          地址: <span>{{ job["Job Address"] }}</span>
        </p>
        <p class="text-gray-700">
          更新日期: <span>{{ job["Appear Date"] }}</span>
        </p>
        <div class="mt-2">
          <span
            v-for="label in job.Labels"
            :key="label"
            class="inline-block text-xs bg-blue-200 text-blue-700 rounded px-2 py-1 mr-2"
          >
            {{ label }}
          </span>
        </div>
        <div class="flex">
          <a
            :href="job['Job Link']"
            target="_blank"
            class="text-indigo-600 hover:text-indigo-800 mt-2 inline-block width-full"
            >查看職位</a
          >
          <span class="text-sm text-gray-500 ml-auto"> # {{ index }}</span>
        </div>
      </li>
    </ul>
  </div>
</template>
