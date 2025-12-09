import { test, expect } from '@playwright/test';

const BASE_URL = process.env.BASE_URL || 'http://localhost:8000';
const TEST_USER = {
  email: `test_${Date.now()}@example.com`,
  username: `testuser_${Date.now()}`,
  password: 'testpass123'
};

test.describe('Profile Management E2E Tests', () => {
  test.beforeEach(async ({ page }) => {
    // Register a new user before each test
    await page.goto(`${BASE_URL}/frontend/register.html`);
    await page.fill('input[name="email"]', TEST_USER.email);
    await page.fill('input[name="username"]', TEST_USER.username);
    await page.fill('input[name="password"]', TEST_USER.password);
    await page.click('button[type="submit"]');
    
    // Wait for redirect to calculations page
    await page.waitForURL('**/frontend/calculations.html');
  });

  test('should view profile information', async ({ page }) => {
    // Navigate to profile page
    await page.goto(`${BASE_URL}/frontend/profile.html`);
    
    // Verify profile information is displayed
    await expect(page.locator('#currentUsername')).toContainText(TEST_USER.username);
    await expect(page.locator('#currentEmail')).toContainText(TEST_USER.email);
    await expect(page.locator('#currentUserId')).not.toBeEmpty();
  });

  test('should update username successfully', async ({ page }) => {
    await page.goto(`${BASE_URL}/frontend/profile.html`);
    
    const newUsername = `updated_${Date.now()}`;
    
    // Update username
    await page.fill('input#username', newUsername);
    await page.click('button[type="submit"]:has-text("Update Profile")');
    
    // Wait for success message
    await expect(page.locator('#profileMessage.success')).toBeVisible();
    await expect(page.locator('#profileMessage')).toContainText('successfully');
    
    // Verify updated username is displayed
    await expect(page.locator('#currentUsername')).toContainText(newUsername);
  });

  test('should update email successfully', async ({ page }) => {
    await page.goto(`${BASE_URL}/frontend/profile.html`);
    
    const newEmail = `updated_${Date.now()}@example.com`;
    
    // Update email
    await page.fill('input#email', newEmail);
    await page.click('button[type="submit"]:has-text("Update Profile")');
    
    // Wait for success message
    await expect(page.locator('#profileMessage.success')).toBeVisible();
    
    // Verify updated email is displayed
    await expect(page.locator('#currentEmail')).toContainText(newEmail);
  });

  test('should update both username and email', async ({ page }) => {
    await page.goto(`${BASE_URL}/frontend/profile.html`);
    
    const newUsername = `updated_${Date.now()}`;
    const newEmail = `updated_${Date.now()}@example.com`;
    
    // Update both fields
    await page.fill('input#username', newUsername);
    await page.fill('input#email', newEmail);
    await page.click('button[type="submit"]:has-text("Update Profile")');
    
    // Wait for success message
    await expect(page.locator('#profileMessage.success')).toBeVisible();
    
    // Verify both fields are updated
    await expect(page.locator('#currentUsername')).toContainText(newUsername);
    await expect(page.locator('#currentEmail')).toContainText(newEmail);
  });

  test('should show error for empty profile update', async ({ page }) => {
    await page.goto(`${BASE_URL}/frontend/profile.html`);
    
    // Try to submit without any changes
    await page.click('button[type="submit"]:has-text("Update Profile")');
    
    // Should show error message
    await expect(page.locator('#profileMessage.error')).toBeVisible();
    await expect(page.locator('#profileMessage')).toContainText('at least one field');
  });

  test('should change password and re-login', async ({ page }) => {
    await page.goto(`${BASE_URL}/frontend/profile.html`);
    
    const newPassword = 'newpass456';
    
    // Fill password change form
    await page.fill('input#currentPassword', TEST_USER.password);
    await page.fill('input#newPassword', newPassword);
    await page.fill('input#confirmPassword', newPassword);
    await page.click('button[type="submit"]:has-text("Change Password")');
    
    // Wait for success message
    await expect(page.locator('#passwordMessage.success')).toBeVisible();
    
    // Should redirect to login page
    await page.waitForURL('**/frontend/login.html', { timeout: 5000 });
    
    // Login with new password
    await page.fill('input[name="username_or_email"]', TEST_USER.username);
    await page.fill('input[name="password"]', newPassword);
    await page.click('button[type="submit"]');
    
    // Should successfully login
    await page.waitForURL('**/frontend/calculations.html');
  });

  test('should show error for wrong current password', async ({ page }) => {
    await page.goto(`${BASE_URL}/frontend/profile.html`);
    
    // Fill password change form with wrong current password
    await page.fill('input#currentPassword', 'wrongpassword');
    await page.fill('input#newPassword', 'newpass456');
    await page.fill('input#confirmPassword', 'newpass456');
    await page.click('button[type="submit"]:has-text("Change Password")');
    
    // Should show error message
    await expect(page.locator('#passwordMessage.error')).toBeVisible();
    await expect(page.locator('#passwordMessage')).toContainText('incorrect');
  });

  test('should validate password mismatch', async ({ page }) => {
    await page.goto(`${BASE_URL}/frontend/profile.html`);
    
    // Fill password change form with mismatched passwords
    await page.fill('input#currentPassword', TEST_USER.password);
    await page.fill('input#newPassword', 'newpass456');
    await page.fill('input#confirmPassword', 'differentpass');
    await page.click('button[type="submit"]:has-text("Change Password")');
    
    // Should show error message
    await expect(page.locator('#passwordMessage.error')).toBeVisible();
    await expect(page.locator('#passwordMessage')).toContainText('do not match');
  });

  test('should validate password length', async ({ page }) => {
    await page.goto(`${BASE_URL}/frontend/profile.html`);
    
    // Fill password change form with short password
    await page.fill('input#currentPassword', TEST_USER.password);
    await page.fill('input#newPassword', 'short');
    await page.fill('input#confirmPassword', 'short');
    await page.click('button[type="submit"]:has-text("Change Password")');
    
    // Should show error message
    await expect(page.locator('#passwordMessage.error')).toBeVisible();
    await expect(page.locator('#passwordMessage')).toContainText('at least 6 characters');
  });

  test('should validate same password', async ({ page }) => {
    await page.goto(`${BASE_URL}/frontend/profile.html`);
    
    // Fill password change form with same password
    await page.fill('input#currentPassword', TEST_USER.password);
    await page.fill('input#newPassword', TEST_USER.password);
    await page.fill('input#confirmPassword', TEST_USER.password);
    await page.click('button[type="submit"]:has-text("Change Password")');
    
    // Should show error message
    await expect(page.locator('#passwordMessage.error')).toBeVisible();
    await expect(page.locator('#passwordMessage')).toContainText('different from current');
  });
});
