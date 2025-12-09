import { test, expect } from '@playwright/test';

const BASE_URL = process.env.BASE_URL || 'http://localhost:8000';

test.describe('Dashboard and Statistics E2E Tests', () => {
  test.beforeEach(async ({ page }) => {
    // Register a new user before each test with unique credentials
    const timestamp = Date.now() + Math.random();
    const TEST_USER = {
      email: `dashboard_${timestamp}@example.com`,
      username: `dashuser_${timestamp}`,
      password: 'testpass123'
    };
    
    await page.goto(`${BASE_URL}/frontend/register.html`);
    await page.fill('input[name="email"]', TEST_USER.email);
    await page.fill('input[name="username"]', TEST_USER.username);
    await page.fill('input[name="password"]', TEST_USER.password);
    await page.click('button[type="submit"]');
    
    // Wait for redirect to calculations page
    await page.waitForURL('**/frontend/calculations.html');
  });

  test('should show empty state when no calculations', async ({ page }) => {
    // Navigate to dashboard
    await page.goto(`${BASE_URL}/frontend/dashboard.html`);
    
    // Should show empty state
    await expect(page.locator('#emptyState')).toBeVisible();
    await expect(page.locator('.empty-state h3')).toContainText('No Calculations Yet');
  });

  test('should display statistics after creating calculations', async ({ page }) => {
    // Create some calculations first
    await page.goto(`${BASE_URL}/frontend/calculations.html`);
    
    // Create 3 Add calculations
    for (let i = 0; i < 3; i++) {
      await page.fill('input#operand1', '10');
      await page.fill('input#operand2', '5');
      await page.selectOption('select#operation', 'Add');
      await page.click('button[type="submit"]:has-text("Calculate")');
      await page.waitForTimeout(500); // Brief pause between operations
    }
    
    // Create 2 Multiply calculations
    for (let i = 0; i < 2; i++) {
      await page.fill('input#operand1', '10');
      await page.fill('input#operand2', '5');
      await page.selectOption('select#operation', 'Multiply');
      await page.click('button[type="submit"]:has-text("Calculate")');
      await page.waitForTimeout(500);
    }
    
    // Navigate to dashboard
    await page.goto(`${BASE_URL}/frontend/dashboard.html`);
    
    // Wait for stats to load
    await expect(page.locator('#statsContent')).toBeVisible();
    
    // Verify total calculations
    await expect(page.locator('#totalCalculations')).toContainText('5');
    
    // Verify most used operation
    await expect(page.locator('#mostUsedOperation')).toContainText('Add');
    
    // Verify operations breakdown is displayed
    await expect(page.locator('.operation-label:has-text("Add")')).toBeVisible();
    await expect(page.locator('.operation-label:has-text("Multiply")')).toBeVisible();
  });

  test('should show all six operation types in breakdown', async ({ page }) => {
    // Create calculations with all operation types
    await page.goto(`${BASE_URL}/frontend/calculations.html`);
    
    const operations = [
      { name: 'Add', a: '10', b: '5' },
      { name: 'Sub', a: '10', b: '5' },
      { name: 'Multiply', a: '10', b: '5' },
      { name: 'Divide', a: '10', b: '5' },
      { name: 'Power', a: '2', b: '3' },
      { name: 'Modulus', a: '10', b: '3' }
    ];
    
    for (const op of operations) {
      await page.fill('input#operand1', op.a);
      await page.fill('input#operand2', op.b);
      await page.selectOption('select#operation', op.name);
      await page.click('button[type="submit"]:has-text("Calculate")');
      await page.waitForTimeout(500);
    }
    
    // Navigate to dashboard
    await page.goto(`${BASE_URL}/frontend/dashboard.html`);
    
    // Wait for stats to load
    await expect(page.locator('#statsContent')).toBeVisible();
    
    // Verify all operations are shown in breakdown
    for (const op of operations) {
      await expect(page.locator(`.operation-label:has-text("${op.name}")`)).toBeVisible();
    }
    
    // Verify total is 6
    await expect(page.locator('#totalCalculations')).toContainText('6');
  });

  test('should calculate correct average result', async ({ page }) => {
    // Create calculations with known results
    await page.goto(`${BASE_URL}/frontend/calculations.html`);
    
    // 10 + 0 = 10
    await page.fill('input#operand1', '10');
    await page.fill('input#operand2', '0');
    await page.selectOption('select#operation', 'Add');
    await page.click('button[type="submit"]:has-text("Calculate")');
    await page.waitForTimeout(500);
    
    // 20 + 0 = 20
    await page.fill('input#operand1', '20');
    await page.fill('input#operand2', '0');
    await page.selectOption('select#operation', 'Add');
    await page.click('button[type="submit"]:has-text("Calculate")');
    await page.waitForTimeout(500);
    
    // 30 + 0 = 30
    await page.fill('input#operand1', '30');
    await page.fill('input#operand2', '0');
    await page.selectOption('select#operation', 'Add');
    await page.click('button[type="submit"]:has-text("Calculate")');
    await page.waitForTimeout(500);
    
    // Navigate to dashboard
    await page.goto(`${BASE_URL}/frontend/dashboard.html`);
    
    // Wait for stats to load
    await expect(page.locator('#statsContent')).toBeVisible();
    
    // Average should be (10 + 20 + 30) / 3 = 20
    await expect(page.locator('#averageResult')).toContainText('20.00');
  });

  test('should update statistics when new calculations added', async ({ page }) => {
    // Create initial calculations
    await page.goto(`${BASE_URL}/frontend/calculations.html`);
    
    await page.fill('input#operand1', '10');
    await page.fill('input#operand2', '5');
    await page.selectOption('select#operation', 'Add');
    await page.click('button[type="submit"]:has-text("Calculate")');
    await page.waitForTimeout(500);
    
    // Check initial stats
    await page.goto(`${BASE_URL}/frontend/dashboard.html`);
    await expect(page.locator('#totalCalculations')).toContainText('1');
    
    // Go back and add more calculations
    await page.goto(`${BASE_URL}/frontend/calculations.html`);
    
    await page.fill('input#operand1', '20');
    await page.fill('input#operand2', '10');
    await page.selectOption('select#operation', 'Multiply');
    await page.click('button[type="submit"]:has-text("Calculate")');
    await page.waitForTimeout(500);
    
    // Check updated stats
    await page.goto(`${BASE_URL}/frontend/dashboard.html`);
    await expect(page.locator('#totalCalculations')).toContainText('2');
  });

  test('should navigate between dashboard, calculations, and profile', async ({ page }) => {
    await page.goto(`${BASE_URL}/frontend/dashboard.html`);
    
    // Navigate to calculations
    await page.click('a:has-text("My Calculations")');
    await expect(page).toHaveURL(/.*calculations\.html/);
    
    // Navigate to profile
    await page.click('button:has-text("Profile")');
    await expect(page).toHaveURL(/.*profile\.html/);
    
    // Navigate back to dashboard
    await page.click('a:has-text("Dashboard")');
    await expect(page).toHaveURL(/.*dashboard\.html/);
  });

  test('should show progress bars in operations breakdown', async ({ page }) => {
    // Create calculations with varying counts
    await page.goto(`${BASE_URL}/frontend/calculations.html`);
    
    // Create 5 Add operations
    for (let i = 0; i < 5; i++) {
      await page.fill('input#operand1', '10');
      await page.fill('input#operand2', '5');
      await page.selectOption('select#operation', 'Add');
      await page.click('button[type="submit"]:has-text("Calculate")');
      await page.waitForTimeout(300);
    }
    
    // Create 2 Multiply operations
    for (let i = 0; i < 2; i++) {
      await page.fill('input#operand1', '10');
      await page.fill('input#operand2', '5');
      await page.selectOption('select#operation', 'Multiply');
      await page.click('button[type="submit"]:has-text("Calculate")');
      await page.waitForTimeout(300);
    }
    
    // Navigate to dashboard
    await page.goto(`${BASE_URL}/frontend/dashboard.html`);
    await expect(page.locator('#statsContent')).toBeVisible();
    
    // Check that bars are displayed
    const addBar = page.locator('.operation-bar:has(.operation-label:has-text("Add"))');
    await expect(addBar).toBeVisible();
    await expect(addBar.locator('.bar-count')).toContainText('5');
    
    const multiplyBar = page.locator('.operation-bar:has(.operation-label:has-text("Multiply"))');
    await expect(multiplyBar).toBeVisible();
    await expect(multiplyBar.locator('.bar-count')).toContainText('2');
  });

  test('should require authentication to view dashboard', async ({ page, context }) => {
    // Clear cookies (logout)
    await context.clearCookies();
    
    // Try to access dashboard without being logged in
    await page.goto(`${BASE_URL}/frontend/dashboard.html`);
    
    // Should redirect to login page
    await page.waitForURL('**/frontend/login.html');
  });
});
