<template>
  <div id="app">
    <h1>Job Scraper</h1>

    <p>已抓到 {{ pageCount }} 頁資料</p>

    <h3>爬取的工作列表：</h3>
    <ul>
      <li v-for="job in jobs" :key="job['Job Link']">
        {{ job["Job Name"] }}
        <br />
        公司名稱: {{ job["Company Name"] }}
        <br />
        地址: {{ job["Job Address"] }}
        <br />
        <a :href="job['Job Link']" target="_blank">查看職位</a>
      </li>
    </ul>
  </div>
</template>

<script>
  export default {
    data() {
      return {
        pageCount: 0, // 用來顯示抓取的頁數
        jobs: [], // 存儲爬取的工作資料
      };
    },
    mounted() {
      // 開始接收 SSE 事件
      const eventSource = new EventSource("http://localhost:5000/api/jobs"); // 後端 SSE 連結

      eventSource.onmessage = (event) => {
        const data = JSON.parse(event.data); // 確保資料是合法的 JSON 格式

        // 更新已抓取的頁數
        if (data.page_count !== undefined) {
          this.pageCount = data.page_count;
        }

        // 如果收到了所有的資料，將資料顯示在頁面上
        if (data.jobs) {
          this.jobs = data.jobs; // 存儲爬取的資料
          eventSource.close(); // 完成後關閉 SSE 連接
        }
      };

      eventSource.onerror = () => {
        console.error("Error occurred while receiving the event");
        eventSource.close(); // 在出錯時關閉 SSE 連接
      };
    },
  };
</script>

<style>
  /* 一些簡單的樣式 */
</style>
