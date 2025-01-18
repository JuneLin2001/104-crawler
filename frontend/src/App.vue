<script lang="ts">
  import Card from "./components/Card.vue";
  import ProgressBar from "./components/ProgressBar.vue";

  interface Job {
    "Job Name": string;
    Description: string;
    "Job Address": string;
    "Job Link": string;
    "Appear Date": string;
    "Company Name": string;
    Labels: string[];
  }

  export default {
    name: "App",
    components: {
      Card,
      ProgressBar,
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
        return this.jobResults;
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
      符合條件的共有 {{ totalItems }} 個工作
    </p>

    <ProgressBar :progress="progress" />

    <div>
      <Card
        v-for="(job, index) in normalJobs"
        :key="job['Job Link']"
        :job="job"
        :index="index + 1"
      />
    </div>
  </div>
</template>
