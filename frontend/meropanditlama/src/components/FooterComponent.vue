<template>
  <footer class="footer">
    <div class="footer-content">
      <div class="footer-section">
        <h3 class="footer-title">Contact Information</h3>
        <p class="footer-text">Email: support@meropanditlama.com</p>
        <p class="footer-text">Phone: +977 9800000806</p>
        <p class="footer-text">Kathmandu, Nepal</p>
      </div>
      <div class="footer-section">
        <h3 class="footer-title">Need Help?</h3>
        <p class="footer-text">Our team is here to guide you</p>
        <router-link to="/help" class="contact-support-link">Contact Support</router-link>
      </div>
    </div>
  </footer>
</template>

<script>
</script>

<style scoped>
.footer {
  background: white;
  border-top: 1px solid #E5E7EB;
  padding: 40px;
  margin-top: auto;
  text-align: center;
}

.footer-content {
  max-width: 1200px;
  margin: 0 auto;
  display: flex;
  justify-content: space-between;
  gap: 60px;
}

.footer-section {
  flex: 1;
}

.footer-title {
  font-size: 16px;
  font-weight: 600;
  color: #000;
  margin-bottom: 16px;
}

.footer-text {
  font-size: 14px;
  color: #666;
  margin-bottom: 8px;
  line-height: 1.6;
}

.contact-support-link {
  display: inline-block;
  margin-top: 8px;
  color: #AE664A;
  text-decoration: none;
  font-weight: 500;
  font-size: 14px;
  cursor: pointer;
}

.contact-support-link:hover {
  text-decoration: underline;
}

@media (max-width: 768px) {
  .footer-content {
    flex-direction: column;
    gap: 30px;
  }
}
</style>
