<script>
  import ProgressBar from "./components/ProgressBar.vue";
  import Card from "./components/Card.vue";

  export default {
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
    <Card v-for="job in jobs" :key="job['Job Link']" :job="job" />
  </div>
</template>
