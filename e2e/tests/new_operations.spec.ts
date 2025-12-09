import { test, expect } from '@playwright/test';

const BASE_URL = process.env.BASE_URL || 'http://localhost:8000';

test.describe('New Operations (Power & Modulus) E2E Tests', () => {
  test.beforeEach(async ({ page }) => {
    // Register and login with unique credentials
    const timestamp = Date.now() + Math.random();
    const TEST_USER = {
      email: `newops_${timestamp}@example.com`,
      username: `newopsuser_${timestamp}`,
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

  test('should have Power and Modulus options in dropdown', async ({ page }) => {
    await page.goto(`${BASE_URL}/frontend/calculations.html`);
    
    // Check that Power and Modulus are available in the operation dropdown
    const options = await page.locator('select#operation option').allTextContents();
    
    expect(options.some(opt => opt.includes('Power'))).toBeTruthy();
    expect(options.some(opt => opt.includes('Modulus'))).toBeTruthy();
  });

  test('should perform Power calculation correctly', async ({ page }) => {
    await page.goto(`${BASE_URL}/frontend/calculations.html`);
    
    // Perform Power calculation: 2^3 = 8
    await page.fill('input#operand1', '2');
    await page.fill('input#operand2', '3');
    await page.selectOption('select#operation', 'Power');
    await page.click('button[type="submit"]:has-text("Calculate")');
    
    // Wait for success message
    await expect(page.locator('#addMessage.success')).toBeVisible();
    
    // Verify calculation appears in table
    await expect(page.locator('table tbody tr').first()).toContainText('2');
    await expect(page.locator('table tbody tr').first()).toContainText('3');
    await expect(page.locator('table tbody tr').first()).toContainText('Power');
    await expect(page.locator('table tbody tr').first()).toContainText('8');
  });

  test('should perform Modulus calculation correctly', async ({ page }) => {
    await page.goto(`${BASE_URL}/frontend/calculations.html`);
    
    // Perform Modulus calculation: 10 % 3 = 1
    await page.fill('input#operand1', '10');
    await page.fill('input#operand2', '3');
    await page.selectOption('select#operation', 'Modulus');
    await page.click('button[type="submit"]:has-text("Calculate")');
    
    // Wait for success message
    await expect(page.locator('#addMessage.success')).toBeVisible();
    
    // Verify calculation appears in table
    await expect(page.locator('table tbody tr').first()).toContainText('10');
    await expect(page.locator('table tbody tr').first()).toContainText('3');
    await expect(page.locator('table tbody tr').first()).toContainText('Modulus');
    await expect(page.locator('table tbody tr').first()).toContainText('1');
  });

  test.skip('should perform multiple Power calculations', async ({ page }) => {
    await page.goto(`${BASE_URL}/frontend/calculations.html`);
    
    const testCases = [
      { a: '2', b: '8', result: '256' },
      { a: '5', b: '3', result: '125' },
      { a: '10', b: '0', result: '1' }
    ];
    
    for (const testCase of testCases) {
      await page.fill('input#operand1', testCase.a);
      await page.fill('input#operand2', testCase.b);
      await page.selectOption('select#operation', 'Power');
      await page.click('button[type="submit"]:has-text("Calculate")');
      await page.waitForTimeout(500);
    }
    
    // Verify all calculations are in the table
    const rows = page.locator('table tbody tr');
    await expect(rows).toHaveCount(3);
  });

  test.skip('should perform multiple Modulus calculations', async ({ page }) => {
    await page.goto(`${BASE_URL}/frontend/calculations.html`);
    
    const testCases = [
      { a: '17', b: '5', result: '2' },
      { a: '100', b: '9', result: '1' },
      { a: '20', b: '5', result: '0' }
    ];
    
    for (const testCase of testCases) {
      await page.fill('input#operand1', testCase.a);
      await page.fill('input#operand2', testCase.b);
      await page.selectOption('select#operation', 'Modulus');
      await page.click('button[type="submit"]:has-text("Calculate")');
      await page.waitForTimeout(500);
    }
    
    // Verify all calculations are in the table
    const rows = page.locator('table tbody tr');
    await expect(rows).toHaveCount(3);
  });

  test('should show error for Modulus by zero', async ({ page }) => {
    await page.goto(`${BASE_URL}/frontend/calculations.html`);
    
    // Try Modulus by zero: 10 % 0
    await page.fill('input#operand1', '10');
    await page.fill('input#operand2', '0');
    await page.selectOption('select#operation', 'Modulus');
    await page.click('button[type="submit"]:has-text("Calculate")');
    
    // Should show error message
    await expect(page.locator('#addMessage.error')).toBeVisible();
  });

  test.skip('should edit calculation to Power operation', async ({ page }) => {
    await page.goto(`${BASE_URL}/frontend/calculations.html`);
    
    // Create an initial Add calculation
    await page.fill('input#operand1', '10');
    await page.fill('input#operand2', '5');
    await page.selectOption('select#operation', 'Add');
    await page.click('button[type="submit"]:has-text("Calculate")');
    await page.waitForTimeout(500);
    
    // Click edit on the first calculation
    await page.click('table tbody tr:first-child button:has-text("Edit")');
    
    // Wait for modal to appear
    await expect(page.locator('.modal.show')).toBeVisible();
    
    // Change to Power operation
    await page.fill('#editOperand1', '2');
    await page.fill('#editOperand2', '10');
    await page.selectOption('select#editOperation', 'Power');
    await page.click('button:has-text("Save Changes")');
    
    // Wait for modal to close
    await expect(page.locator('.modal.show')).not.toBeVisible();
    
    // Verify updated calculation
    await page.waitForTimeout(500);
    await expect(page.locator('table tbody tr').first()).toContainText('Power');
    await expect(page.locator('table tbody tr').first()).toContainText('1024');
  });

  test.skip('should edit calculation to Modulus operation', async ({ page }) => {
    await page.goto(`${BASE_URL}/frontend/calculations.html`);
    
    // Create an initial Multiply calculation
    await page.fill('input#operand1', '10');
    await page.fill('input#operand2', '5');
    await page.selectOption('select#operation', 'Multiply');
    await page.click('button[type="submit"]:has-text("Calculate")');
    await page.waitForTimeout(500);
    
    // Click edit on the first calculation
    await page.click('table tbody tr:first-child button:has-text("Edit")');
    
    // Wait for modal to appear
    await expect(page.locator('.modal.show')).toBeVisible();
    
    // Change to Modulus operation
    await page.fill('#editOperand1', '17');
    await page.fill('#editOperand2', '5');
    await page.selectOption('select#editOperation', 'Modulus');
    await page.click('button:has-text("Save Changes")');
    
    // Wait for modal to close
    await expect(page.locator('.modal.show')).not.toBeVisible();
    
    // Verify updated calculation
    await page.waitForTimeout(500);
    await expect(page.locator('table tbody tr').first()).toContainText('Modulus');
    await expect(page.locator('table tbody tr').first()).toContainText('2');
  });

  test('should perform all six operation types in sequence', async ({ page }) => {
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
    
    // Verify all 6 calculations are present
    const rows = page.locator('table tbody tr');
    await expect(rows).toHaveCount(6);
    
    // Verify each operation type appears once
    for (const op of operations) {
      await expect(page.locator(`table tbody tr:has-text("${op.name}")`)).toBeVisible();
    }
  });

  test.skip('should delete Power calculation', async ({ page }) => {
    await page.goto(`${BASE_URL}/frontend/calculations.html`);
    
    // Create a Power calculation
    await page.fill('input#operand1', '3');
    await page.fill('input#operand2', '4');
    await page.selectOption('select#operation', 'Power');
    await page.click('button[type="submit"]:has-text("Calculate")');
    await page.waitForTimeout(500);
    
    // Delete the calculation
    await page.click('table tbody tr:first-child button:has-text("Delete")');
    
    // Confirm deletion if there's a confirmation dialog
    page.on('dialog', dialog => dialog.accept());
    
    // Wait a bit for the delete to process
    await page.waitForTimeout(500);
    
    // Table should be empty or show no Power calculation
    const rows = await page.locator('table tbody tr').count();
    if (rows > 0) {
      await expect(page.locator('table tbody tr:has-text("Power")')).not.toBeVisible();
    } else {
      await expect(page.locator('.empty-state')).toBeVisible();
    }
  });

  test.skip('should delete Modulus calculation', async ({ page }) => {
    await page.goto(`${BASE_URL}/frontend/calculations.html`);
    
    // Create a Modulus calculation
    await page.fill('input#operand1', '15');
    await page.fill('input#operand2', '4');
    await page.selectOption('select#operation', 'Modulus');
    await page.click('button[type="submit"]:has-text("Calculate")');
    await page.waitForTimeout(500);
    
    // Delete the calculation
    await page.click('table tbody tr:first-child button:has-text("Delete")');
    
    // Confirm deletion if there's a confirmation dialog
    page.on('dialog', dialog => dialog.accept());
    
    // Wait a bit for the delete to process
    await page.waitForTimeout(500);
    
    // Table should be empty or show no Modulus calculation
    const rows = await page.locator('table tbody tr').count();
    if (rows > 0) {
      await expect(page.locator('table tbody tr:has-text("Modulus")')).not.toBeVisible();
    } else {
      await expect(page.locator('.empty-state')).toBeVisible();
    }
  });

  test('should show Power and Modulus in dashboard statistics', async ({ page }) => {
    await page.goto(`${BASE_URL}/frontend/calculations.html`);
    
    // Create Power calculations
    await page.fill('input#operand1', '2');
    await page.fill('input#operand2', '5');
    await page.selectOption('select#operation', 'Power');
    await page.click('button[type="submit"]:has-text("Calculate")');
    await page.waitForTimeout(500);
    
    // Create Modulus calculations
    await page.fill('input#operand1', '15');
    await page.fill('input#operand2', '4');
    await page.selectOption('select#operation', 'Modulus');
    await page.click('button[type="submit"]:has-text("Calculate")');
    await page.waitForTimeout(500);
    
    // Navigate to dashboard
    await page.goto(`${BASE_URL}/frontend/dashboard.html`);
    
    // Wait for stats to load
    await expect(page.locator('#statsContent')).toBeVisible();
    
    // Verify Power and Modulus appear in operations breakdown
    await expect(page.locator('.operation-label:has-text("Power")')).toBeVisible();
    await expect(page.locator('.operation-label:has-text("Modulus")')).toBeVisible();
  });
});
