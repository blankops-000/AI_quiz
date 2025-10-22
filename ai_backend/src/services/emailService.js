// ============================================
// FILE: src/services/emailService.js
// ============================================
const nodemailer = require('nodemailer');
const logger = require('../utils/logger');

class EmailService {
  constructor() {
    this.transporter = nodemailer.createTransport({
      host: process.env.EMAIL_HOST || 'smtp.gmail.com',
      port: process.env.EMAIL_PORT || 587,
      secure: false,
      auth: {
        user: process.env.EMAIL_USER,
        pass: process.env.EMAIL_PASSWORD
      }
    });
  }

  async sendEmail(to, subject, html, text) {
    try {
      const mailOptions = {
        from: `"${process.env.APP_NAME || 'MERN App'}" <${process.env.EMAIL_FROM || process.env.EMAIL_USER}>`,
        to,
        subject,
        html,
        text
      };

      const info = await this.transporter.sendMail(mailOptions);
      logger.info(`Email sent: ${info.messageId}`);
      return info;
    } catch (error) {
      logger.error(`Email sending failed: ${error.message}`);
      throw error;
    }
  }

  async sendWelcomeEmail(user) {
    const subject = 'Welcome to Our Platform!';
    const html = `
      <h1>Welcome ${user.username}!</h1>
      <p>Thank you for registering with us.</p>
      <p>We're excited to have you on board.</p>
    `;
    const text = `Welcome ${user.username}! Thank you for registering with us.`;

    return await this.sendEmail(user.email, subject, html, text);
  }

  async sendPasswordResetEmail(user, resetToken) {
    const subject = 'Password Reset Request';
    const resetUrl = `${process.env.FRONTEND_URL}/reset-password/${resetToken}`;
    const html = `
      <h1>Password Reset</h1>
      <p>You requested a password reset.</p>
      <p>Click the link below to reset your password:</p>
      <a href="${resetUrl}">${resetUrl}</a>
      <p>If you didn't request this, please ignore this email.</p>
    `;
    const text = `Password reset link: ${resetUrl}`;

    return await this.sendEmail(user.email, subject, html, text);
  }
}

module.exports = new EmailService();
