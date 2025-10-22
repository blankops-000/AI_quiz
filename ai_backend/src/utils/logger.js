
// ============================================
// FILE: src/utils/logger.js
// ============================================
const colors = {
  reset: '\x1b[0m',
  bright: '\x1b[1m',
  red: '\x1b[31m',
  green: '\x1b[32m',
  yellow: '\x1b[33m',
  blue: '\x1b[34m',
  cyan: '\x1b[36m'
};

class Logger {
  constructor() {
    this.isDevelopment = process.env.NODE_ENV === 'development';
  }

  formatMessage(level, message) {
    const timestamp = new Date().toISOString();
    return `[${timestamp}] [${level}]: ${message}`;
  }

  info(message) {
    const formatted = this.formatMessage('INFO', message);
    if (this.isDevelopment) {
      console.log(`${colors.blue}${formatted}${colors.reset}`);
    } else {
      console.log(formatted);
    }
  }

  error(message) {
    const formatted = this.formatMessage('ERROR', message);
    if (this.isDevelopment) {
      console.error(`${colors.red}${formatted}${colors.reset}`);
    } else {
      console.error(formatted);
    }
  }

  warn(message) {
    const formatted = this.formatMessage('WARN', message);
    if (this.isDevelopment) {
      console.warn(`${colors.yellow}${formatted}${colors.reset}`);
    } else {
      console.warn(formatted);
    }
  }

  success(message) {
    const formatted = this.formatMessage('SUCCESS', message);
    if (this.isDevelopment) {
      console.log(`${colors.green}${formatted}${colors.reset}`);
    } else {
      console.log(formatted);
    }
  }

  debug(message) {
    if (this.isDevelopment) {
      const formatted = this.formatMessage('DEBUG', message);
      console.log(`${colors.cyan}${formatted}${colors.reset}`);
    }
  }
}

module.exports = new Logger();