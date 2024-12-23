<script lang="ts">
  import ProgressBar from "./components/ProgressBar.vue";
  import Card from "./components/Card.vue";

  export default {
    name: "App",
    components: {
      ProgressBar,
      Card,
    },

    data() {
      return {
        progress: 0,
        pageCount: 0,
        totalPages: 0,
        totalItems: 0,
        jobs: [],
        filtered_out_jobs: [],
        showFilteredOut: false,
      };
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

        if (data.jobs) {
          this.jobs = data.jobs;
          eventSource.close();
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
    computed: {
      filteredOutJobs() {
        return this.showFilteredOut ? this.filtered_out_jobs : this.jobs;
      },
    },
  };
</script>

<template>
  <div id="app" class="max-w-4xl mx-auto p-6">
    <p class="text-xl text-gray-700 mb-4">
      已抓到 {{ pageCount }} 頁資料，共 {{ totalPages }} 頁
    </p>
    <p class="text-xl text-gray-700 mb-4">共有 {{ totalItems }} 個工作</p>

    <ProgressBar :progress="progress" />

    <h3 class="text-2xl text-gray-800 mt-6">爬取的工作列表：</h3>

    <div class="mt-6">
      <label>
        <input type="radio" v-model="showFilteredOut" :value="true" />
        顯示過濾掉的工作
      </label>
      <label class="ml-4">
        <input type="radio" v-model="showFilteredOut" :value="false" />
        顯示正常工作
      </label>
    </div>

    <Card
      v-for="(job, index) in filteredOutJobs"
      :key="job['Job Link']"
      :job="job"
      :index="index + 1"
    />
  </div>
</template>
