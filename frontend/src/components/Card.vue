<script lang="ts">
  import Tag from "primevue/tag";
  import PrimeCard from "primevue/card";
  import Button from "primevue/button";

  export default {
    name: "Card",
    components: {
      Tag,
      PrimeCard,
      Button,
    },
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
    methods: {
      openJobLink(url: string) {
        window.open(url, "_blank");
      },
    },
  };
</script>

<template>
  <PrimeCard class="mb-4">
    <template #title>
      <h2 class="text-lg font-semibold">{{ job["Company Name"] }}</h2>
    </template>

    <template #content>
      <div class="text-gray-700 space-y-2">
        <p>工作名稱： {{ job["Job Name"] }}</p>
        <p>地址： {{ job["Job Address"] }}</p>
        <p>更新日期： {{ job["Appear Date"] }}</p>
      </div>
    </template>

    <template #footer>
      <div class="flex flex-wrap items-center gap-2 mt-4">
        <div class="flex flex-wrap gap-2">
          <Tag v-for="label in job.Labels" :key="label" rounded class="text-sm">
            {{ label }}
          </Tag>
        </div>

        <div class="ml-auto flex items-center gap-4">
          <Button
            label="查看職位"
            @click="openJobLink(job['Job Link'])"
            rounded
            severity="success"
            class="text-sm"
          />
          <span class="text-sm text-gray-500">#{{ index }}</span>
        </div>
      </div>
    </template>
  </PrimeCard>
</template>
