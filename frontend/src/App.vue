<script lang="ts">
  import Card from "./components/Card.vue";
  import ProgressBar from "./components/ProgressBar.vue";
  import RadioButton from "primevue/radiobutton";

  interface Job {
    "Job Name": string;
    Description: string;
    "Job Address": string;
    "Job Link": string;
    "Appear Date": string;
    "Company Name": string;
    Labels: string[];
    isFiltered: boolean;
  }

  export default {
    name: "App",
    components: {
      Card,
      ProgressBar,
      RadioButton,
    },
    data() {
      return {
        jobResults: [] as Job[],
        showFilteredOut: false,
        pageCount: 0,
        totalPages: 0,
        progress: 0,
        totalItems: 0,
      };
    },
    computed: {
      normalJobs() {
        return this.jobResults.filter((job) => !job.isFiltered);
      },
      filteredJobs() {
        return this.jobResults.filter((job) => job.isFiltered);
      },
    },
    mounted() {
      const eventSource = new EventSource("http://localhost:5000/api/jobs");

      eventSource.onmessage = (event) => {
        const data = JSON.parse(event.data);

        if (data.page_count !== undefined && data.total_pages !== undefined) {
          this.pageCount = data.page_count;
          this.totalPages = data.total_pages;
          this.progress = (this.pageCount / this.totalPages) * 100;
        }

        if (data.job_results) {
          this.jobResults = [...this.jobResults, ...data.job_results];
        }

        if (data.metadata) {
          this.totalPages = data.metadata.lastPage;
          this.totalItems = data.metadata.total;
        }
      };

      eventSource.onerror = () => {
        console.error("Error occurred while receiving the event");
        eventSource.close();
      };
    },
  };
</script>

<template>
  <div id="app" class="max-w-4xl mx-auto p-6">
    <p class="text-xl text-gray-700 mb-4">
      已抓到 {{ pageCount }} 頁資料，共 {{ totalPages }} 頁
    </p>

    <p class="text-xl text-gray-700 mb-4">
      符合條件的共有 {{ totalItems }} 個工作，過濾了
      {{ filteredJobs.length }} 個工作
    </p>

    <ProgressBar :progress="progress" />

    <div class="flex flex-wrap gap-4">
      <div class="flex items-center gap-2">
        <RadioButton
          v-model="showFilteredOut"
          inputId="filter1"
          name="jobFilter"
          :value="true"
        />
        <label for="filter1">顯示過濾掉的工作</label>
      </div>
      <div class="flex items-center gap-2">
        <RadioButton
          v-model="showFilteredOut"
          inputId="filter2"
          name="jobFilter"
          :value="false"
        />
        <label for="filter2">顯示符合條件的工作</label>
      </div>
    </div>

    <div>
      <h2 class="mt-6 text-xl">
        {{ showFilteredOut ? "過濾掉的工作" : "符合條件的工作" }}
      </h2>
      <Card
        v-for="(job, index) in showFilteredOut ? filteredJobs : normalJobs"
        :key="job['Job Link']"
        :job="job"
        :index="index + 1"
      />
    </div>
  </div>
</template>
