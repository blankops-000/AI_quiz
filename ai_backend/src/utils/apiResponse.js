
// ============================================
// FILE: src/utils/apiResponse.js
// ============================================
class ApiResponse {
  static success(data = null, message = 'Success', statusCode = 200) {
    return {
      success: true,
      message,
      data,
      statusCode
    };
  }

  static error(message = 'Error', statusCode = 500, errors = null) {
    return {
      success: false,
      message,
      errors,
      statusCode
    };
  }

  static paginated(data, pagination, message = 'Success') {
    return {
      success: true,
      message,
      data,
      pagination
    };
  }
}

module.exports = { ApiResponse };
