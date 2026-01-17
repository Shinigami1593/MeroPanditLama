<template>
  <div class="help-page">
    <Navbar :isAuthenticated="true" />

    <main class="main-content">
      <div class="help-container">
        <h1 class="help-title">Help & Support</h1>
        <p class="help-subtitle">Learn how to use MeroPanditLama</p>

        <!-- Video Tutorial Section -->
        <div class="video-section">
          <h2 class="section-title">Video Tutorial</h2>
          <div class="video-wrapper">
            <iframe
              class="video-iframe"
              src="https://youtube.com/embed/BCP7SmWmI8E"
              title="MeroPanditLama Tutorial"
              frameborder="0"
              allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
              allowfullscreen
            ></iframe>
          </div>
        </div>

        <!-- FAQ Section -->
        <div class="faq-section">
          <h2 class="section-title">Frequently Asked Questions</h2>

          <div class="faq-item">
            <h3 class="faq-question">How do I book a Pandit or Lama?</h3>
            <p class="faq-answer">
              Browse available providers, select your preferred date and time slot,
              choose a service, and submit your booking request. The provider will
              confirm your booking.
            </p>
          </div>

          <div class="faq-item">
            <h3 class="faq-question">Can I cancel my booking?</h3>
            <p class="faq-answer">
              Yes, you can cancel pending or confirmed bookings from your "My Bookings"
              page. Please note our cancellation policy.
            </p>
          </div>

          <div class="faq-item">
            <h3 class="faq-question">How do I contact a provider?</h3>
            <p class="faq-answer">
              Once your booking is confirmed, you can contact the provider directly
              using the phone number provided in your booking details.
            </p>
          </div>

          <div class="faq-item">
            <h3 class="faq-question">What payment methods are accepted?</h3>
            <p class="faq-answer">
              We accept various payment methods including cash payment to the provider
              directly. Online payment options will be available soon.
            </p>
          </div>
        </div>

        <!-- Contact Support Section -->
        <div class="contact-section">
          <h2 class="section-title">Still Need Help?</h2>
          <p class="contact-text">
            Our support team is available to assist you
          </p>
          <div class="contact-info">
            <div class="contact-item">
              <span class="contact-icon">📧</span>
              <div>
                <p class="contact-label">Email</p>
                <a href="mailto:support@meropanditlama.com" class="contact-link">
                  support@meropanditlama.com
                </a>
              </div>
            </div>
            <div class="contact-item">
              <span class="contact-icon">📞</span>
              <div>
                <p class="contact-label">Phone</p>
                <a href="tel:+9779800000806" class="contact-link">
                  +977 9800000806
                </a>
              </div>
            </div>
            <div class="contact-item">
              <span class="contact-icon">📍</span>
              <div>
                <p class="contact-label">Location</p>
                <p class="contact-value">Kathmandu, Nepal</p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </main>

    <Footer />
  </div>
</template>

<script setup>
import Navbar from '@/components/NavbarComponent.vue'
import Footer from '@/components/FooterComponent.vue'
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Rubik:wght@300;400;500;600;700&display=swap');

.help-page {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  background-color: #FFF5E1;
  font-family: 'Rubik', sans-serif;
}

.main-content {
  flex: 1;
  width: 100%;
}

.help-container {
  max-width: 900px;
  margin: 0 auto;
  padding: 60px 40px;
}

.help-title {
  font-size: 36px;
  font-weight: 600;
  color: #AE664A;
  text-align: center;
  margin-bottom: 12px;
}

.help-subtitle {
  font-size: 16px;
  color: #666;
  text-align: center;
  margin-bottom: 50px;
}

.section-title {
  font-size: 24px;
  font-weight: 600;
  color: #AE664A;
  margin-bottom: 24px;
}

/* Video Section */
.video-section {
  margin-bottom: 60px;
}

.video-wrapper {
  position: relative;
  padding-bottom: 56.25%; /* 16:9 aspect ratio */
  height: 0;
  overflow: hidden;
  background: #000;
  border-radius: 12px;
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.1);
}

.video-iframe {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  border-radius: 12px;
}

/* FAQ Section */
.faq-section {
  margin-bottom: 60px;
}

.faq-item {
  background: white;
  padding: 24px;
  border-radius: 12px;
  margin-bottom: 16px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
}

.faq-question {
  font-size: 18px;
  font-weight: 600;
  color: #333;
  margin-bottom: 12px;
}

.faq-answer {
  font-size: 15px;
  color: #666;
  line-height: 1.6;
}

/* Contact Section */
.contact-section {
  background: white;
  padding: 40px;
  border-radius: 12px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.08);
  text-align: center;
}

.contact-text {
  font-size: 16px;
  color: #666;
  margin-bottom: 32px;
}

.contact-info {
  display: flex;
  justify-content: center;
  gap: 40px;
  flex-wrap: wrap;
}

.contact-item {
  display: flex;
  align-items: flex-start;
  gap: 12px;
  text-align: left;
}

.contact-icon {
  font-size: 24px;
}

.contact-label {
  font-size: 12px;
  color: #999;
  margin-bottom: 4px;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.contact-link {
  font-size: 15px;
  color: #AE664A;
  text-decoration: none;
  font-weight: 500;
}

.contact-link:hover {
  text-decoration: underline;
}

.contact-value {
  font-size: 15px;
  color: #333;
}

/* Responsive Design */
@media (max-width: 768px) {
  .help-container {
    padding: 40px 20px;
  }

  .help-title {
    font-size: 28px;
  }

  .section-title {
    font-size: 20px;
  }

  .contact-info {
    flex-direction: column;
    align-items: center;
    gap: 24px;
  }

  .contact-item {
    justify-content: center;
  }
}
</style>
