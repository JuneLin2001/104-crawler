<template>
  <div id="app" class="max-w-4xl mx-auto p-6">
    <h1 class="text-4xl font-bold text-center text-gray-800 mb-6">
      Job Scraper
    </h1>

    <!-- 顯示已抓取頁數、總頁數、總工作數 -->
    <p class="text-xl text-gray-700 mb-4">
      已抓到 {{ pageCount }} 頁資料，共 {{ totalPages }} 頁
    </p>
    <p class="text-xl text-gray-700 mb-4">共抓到 {{ totalItems }} 個工作</p>

    <!-- 進度條 -->
    <div class="w-full bg-gray-200 rounded-full h-4 mb-4">
      <div
        class="bg-green-500 h-4 rounded-full"
        :style="{ width: progress + '%' }"
      ></div>
    </div>
    <p class="text-center text-sm text-gray-600">
      進度: {{ progress.toFixed(2) }}%
    </p>

    <!-- 顯示工作列表 -->
    <h3 class="text-2xl text-gray-800 mt-6">爬取的工作列表：</h3>
    <ul class="space-y-4 mt-4">
      <li
        v-for="job in jobs"
        :key="job['Job Link']"
        class="p-4 border border-gray-200 rounded-lg shadow-md hover:shadow-lg transition duration-300 ease-in-out"
      >
        <h4 class="text-xl text-gray-900">
          {{ job["Job Name"] }}
        </h4>
        <p class="text-gray-700 mt-2">
          公司名稱: <span>{{ job["Company Name"] }}</span>
        </p>
        <p class="text-gray-700">
          地址: <span>{{ job["Job Address"] }}</span>
        </p>
        <a
          :href="job['Job Link']"
          target="_blank"
          class="text-indigo-600 hover:text-indigo-800 mt-2 inline-block"
        >
          查看職位
        </a>
      </li>
    </ul>
  </div>
</template>

<script>
  export default {
    data() {
      return {
        progress: 0, // 進度條百分比
        pageCount: 0, // 已抓取的頁數
        totalPages: 0, // 總頁數
        totalItems: 0, // 總項目數
        jobs: [], // 存儲爬取的工作資料
      };
    },
    mounted() {
      // 開始接收 SSE 事件
      const eventSource = new EventSource("http://localhost:5000/api/jobs"); // 後端 SSE 連結

      eventSource.onmessage = (event) => {
        const data = JSON.parse(event.data); // 確保資料是合法的 JSON 格式

        // 更新已抓取的頁數和總頁數
        if (data.page_count !== undefined && data.total_pages !== undefined) {
          this.pageCount = data.page_count;
          this.totalPages = data.total_pages;
          this.totalItems = data.total_items; // 更新總項目數
          this.progress = (this.pageCount / this.totalPages) * 100; // 計算進度條百分比
        }

        // 如果收到了所有的資料，將資料顯示在頁面上
        if (data.jobs) {
          this.jobs = data.jobs; // 存儲爬取的資料
          eventSource.close(); // 完成後關閉 SSE 連接
        }

        // 如果 metadata 被傳送，顯示總頁數等
        if (data.metadata) {
          this.totalPages = data.metadata.lastPage;
          this.totalItems = data.metadata.total;
        }
      };

      eventSource.onerror = () => {
        console.error("Error occurred while receiving the event");
        eventSource.close(); // 在出錯時關閉 SSE 連接
      };
    },
  };
</script>

<style scoped>
  /* 這裡使用 Tailwind 的樣式，不需要再額外添加樣式 */
</style>
