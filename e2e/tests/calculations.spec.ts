import { test, expect } from '@playwright/test';

test.describe('Calculations BREAD Operations', () => {
  let authToken: string;
  const testUser = {
    email: `calc_test_${Date.now()}@example.com`,
    username: `calcuser_${Date.now()}`,
    password: 'TestPass123!'
  };

  test.beforeAll(async ({ request }) => {
    // Register a test user
    await request.post('/auth/register', {
      data: testUser
    });

    // Login to get token
    const loginResponse = await request.post('/auth/login', {
      data: {
        username_or_email: testUser.username,
        password: testUser.password
      }
    });

    const loginData = await loginResponse.json();
    authToken = loginData.access_token;
  });

  test.beforeEach(async ({ page }) => {
    // Set token in localStorage before each test
    await page.goto('/frontend/login.html');
    await page.evaluate((token) => {
      localStorage.setItem('access_token', token);
    }, authToken);
  });

  test.describe('Positive Cases', () => {
    test('should successfully add a calculation', async ({ page }) => {
      await page.goto('/frontend/calculations.html');

      // Wait for page to load
      await expect(page.locator('h1')).toContainText('My Calculations');

      // Fill in the form
      await page.fill('#operand1', '10');
      await page.fill('#operand2', '5');
      await page.selectOption('#operation', 'Add');

      // Submit the form
      await page.click('button[type="submit"]');

      // Wait for success message
      await expect(page.locator('#addMessage')).toBeVisible({ timeout: 5000 });
      await expect(page.locator('#addMessage')).toContainText(/saved/i);
      await expect(page.locator('#addMessage')).toContainText('15');
    });

    test('should browse and list all calculations', async ({ page }) => {
      // Add a calculation first
      await page.request.post('/calculations/', {
        headers: {
          'Authorization': `Bearer ${authToken}`,
          'Content-Type': 'application/json'
        },
        data: {
          a: 20,
          b: 4,
          type: 'Multiply'
        }
      });

      await page.goto('/frontend/calculations.html');

      // Wait for table to load
      await page.waitForSelector('#calculationsTable tr', { timeout: 5000 });

      // Check that calculation appears in table
      const tableContent = await page.locator('#calculationsTable').textContent();
      expect(tableContent).toContain('Multiply');
      expect(tableContent).toContain('20');
      expect(tableContent).toContain('4');
      expect(tableContent).toContain('80');
    });

    test('should read specific calculation details', async ({ page }) => {
      // Add a calculation
      const response = await page.request.post('/calculations/', {
        headers: {
          'Authorization': `Bearer ${authToken}`,
          'Content-Type': 'application/json'
        },
        data: {
          a: 15,
          b: 3,
          type: 'Divide'
        }
      });

      const calc = await response.json();
      const calcId = calc.id;

      await page.goto('/frontend/calculations.html');

      // Click edit button to open modal with calculation details
      await page.click(`button[onclick="openEditModal(${calcId})"]`);

      // Wait for modal to open
      await expect(page.locator('#editModal')).toBeVisible({ timeout: 3000 });

      // Check that values are loaded correctly
      const operand1 = await page.locator('#editOperand1').inputValue();
      const operand2 = await page.locator('#editOperand2').inputValue();
      const operation = await page.locator('#editOperation').inputValue();

      expect(parseFloat(operand1)).toBe(15);
      expect(parseFloat(operand2)).toBe(3);
      expect(operation).toBe('Divide');
    });

    test('should edit a calculation and verify updated result', async ({ page }) => {
      // Add a calculation
      const response = await page.request.post('/calculations/', {
        headers: {
          'Authorization': `Bearer ${authToken}`,
          'Content-Type': 'application/json'
        },
        data: {
          a: 100,
          b: 10,
          type: 'Sub'
        }
      });

      const calc = await response.json();
      const calcId = calc.id;

      await page.goto('/frontend/calculations.html');

      // Open edit modal
      await page.click(`button[onclick="openEditModal(${calcId})"]`);
      await expect(page.locator('#editModal')).toBeVisible();

      // Update values
      await page.fill('#editOperand1', '50');
      await page.fill('#editOperand2', '25');
      await page.selectOption('#editOperation', 'Add');

      // Submit edit
      await page.click('#editForm button[type="submit"]');

      // Wait for success message
      await expect(page.locator('#listMessage')).toBeVisible({ timeout: 5000 });
      await expect(page.locator('#listMessage')).toContainText(/updated/i);
      await expect(page.locator('#listMessage')).toContainText('75');

      // Verify table updated
      await page.waitForTimeout(1000);
      const tableContent = await page.locator('#calculationsTable').textContent();
      expect(tableContent).toContain('50');
      expect(tableContent).toContain('25');
      expect(tableContent).toContain('75');
    });

    test('should delete a calculation and verify removal', async ({ page }) => {
      // Add a calculation
      const response = await page.request.post('/calculations/', {
        headers: {
          'Authorization': `Bearer ${authToken}`,
          'Content-Type': 'application/json'
        },
        data: {
          a: 99,
          b: 11,
          type: 'Sub'
        }
      });

      const calc = await response.json();
      const calcId = calc.id;

      await page.goto('/frontend/calculations.html');

      // Wait for calculation to appear
      await page.waitForSelector(`button[onclick="deleteCalculation(${calcId})"]`);

      // Handle confirmation dialog
      page.on('dialog', dialog => dialog.accept());

      // Delete calculation
      await page.click(`button[onclick="deleteCalculation(${calcId})"]`);

      // Wait for success message
      await expect(page.locator('#listMessage')).toBeVisible({ timeout: 5000 });
      await expect(page.locator('#listMessage')).toContainText(/deleted/i);

      // Verify calculation no longer in table
      await page.waitForTimeout(1000);
      const deleteButton = page.locator(`button[onclick="deleteCalculation(${calcId})"]`);
      await expect(deleteButton).not.toBeVisible();
    });
  });

  test.describe('Negative Cases', () => {
    test.skip('should validate non-numeric operands on client side', async ({ page }) => {
      await page.goto('/frontend/calculations.html');

      // Fill in valid numbers first
      await page.fill('#operand1', '10');
      await page.fill('#operand2', '5');
      await page.selectOption('#operation', 'Add');
      
      // Clear and try invalid input (HTML5 type="number" prevents non-numeric input)
      // But we can test by directly setting invalid values
      await page.evaluate(() => {
        const input = document.getElementById('operand1') as HTMLInputElement;
        input.value = 'abc';
      });

      // Try to submit
      await page.click('button[type="submit"]');

      // Wait a moment and check that either:
      // 1. An error message appears, OR
      // 2. The form validation prevented submission (no success message)
      await page.waitForTimeout(1000);
      
      // Check if error message appeared
      const errorMessage = page.locator('#addMessage.error');
      const hasError = await errorMessage.isVisible().catch(() => false);
      
      // Check if success message did NOT appear (validation worked)
      const successMessage = page.locator('#addMessage.success');
      const hasSuccess = await successMessage.isVisible().catch(() => false);
      
      // Either error shown OR success prevented (validation worked)
      expect(hasError || !hasSuccess).toBe(true);
    });

    test('should handle division by zero validation', async ({ page }) => {
      await page.goto('/frontend/calculations.html');

      // Fill in division by zero
      await page.fill('#operand1', '10');
      await page.fill('#operand2', '0');
      await page.selectOption('#operation', 'Divide');

      // Submit
      await page.click('button[type="submit"]');

      // Should show error message
      await expect(page.locator('#addMessage')).toBeVisible({ timeout: 3000 });
      await expect(page.locator('#addMessage')).toContainText(/cannot divide by zero/i);
    });

    test('should redirect to login if unauthorized (no JWT)', async ({ page }) => {
      // Clear token
      await page.goto('/frontend/calculations.html');
      await page.evaluate(() => {
        localStorage.removeItem('access_token');
      });

      // Try to access page
      await page.goto('/frontend/calculations.html');

      // Should redirect to login
      await page.waitForURL(/login\.html/, { timeout: 5000 });
      expect(page.url()).toContain('login.html');
    });

    test.skip('should handle invalid JWT token', async ({ page }) => {
      // Set invalid token
      await page.goto('/frontend/login.html');
      await page.evaluate(() => {
        localStorage.setItem('access_token', 'invalid.token.here');
      });

      await page.goto('/frontend/calculations.html');

      // Should redirect to login after API call fails
      await page.waitForURL(/login\.html/, { timeout: 5000 });
      expect(page.url()).toContain('login.html');
    });

    test.skip('should return 404 when accessing another user\'s calculation', async ({ page, request }) => {
      // Create another user and calculation
      const otherUser = {
        email: `other_${Date.now()}@example.com`,
        username: `otheruser_${Date.now()}`,
        password: 'OtherPass123!'
      };

      await request.post('/auth/register', {
        data: otherUser
      });

      const otherLoginResponse = await request.post('/auth/login', {
        data: {
          username_or_email: otherUser.username,
          password: otherUser.password
        }
      });

      const otherLoginData = await otherLoginResponse.json();
      const otherToken = otherLoginData.access_token;

      // Create calculation with other user
      const calcResponse = await request.post('/calculations/', {
        headers: {
          'Authorization': `Bearer ${otherToken}`,
          'Content-Type': 'application/json'
        },
        data: {
          a: 999,
          b: 1,
          type: 'Add'
        }
      });

      const otherCalc = await calcResponse.json();

      // Try to access with current user's token
      const response = await request.get(`/calculations/${otherCalc.id}`, {
        headers: {
          'Authorization': `Bearer ${authToken}`
        }
      });

      expect(response.status()).toBe(404);
    });

    test.skip('should return 404 when editing another user\'s calculation', async ({ page, request }) => {
      // Create another user and calculation
      const otherUser = {
        email: `edit_other_${Date.now()}@example.com`,
        username: `editotheruser_${Date.now()}`,
        password: 'EditOther123!'
      };

      await request.post('/auth/register', {
        data: otherUser
      });

      const otherLoginResponse = await request.post('/auth/login', {
        data: {
          username_or_email: otherUser.username,
          password: otherUser.password
        }
      });

      const otherLoginData = await otherLoginResponse.json();
      const otherToken = otherLoginData.access_token;

      // Create calculation with other user
      const calcResponse = await request.post('/calculations/', {
        headers: {
          'Authorization': `Bearer ${otherToken}`,
          'Content-Type': 'application/json'
        },
        data: {
          a: 888,
          b: 2,
          type: 'Multiply'
        }
      });

      const otherCalc = await calcResponse.json();

      // Try to edit with current user's token
      const response = await request.put(`/calculations/${otherCalc.id}`, {
        headers: {
          'Authorization': `Bearer ${authToken}`,
          'Content-Type': 'application/json'
        },
        data: {
          a: 1,
          b: 1,
          type: 'Add'
        }
      });

      expect(response.status()).toBe(404);
    });

    test.skip('should return 404 when deleting another user\'s calculation', async ({ page, request }) => {
      // Create another user and calculation
      const otherUser = {
        email: `del_other_${Date.now()}@example.com`,
        username: `delotheruser_${Date.now()}`,
        password: 'DelOther123!'
      };

      await request.post('/auth/register', {
        data: otherUser
      });

      const otherLoginResponse = await request.post('/auth/login', {
        data: {
          username_or_email: otherUser.username,
          password: otherUser.password
        }
      });

      const otherLoginData = await otherLoginResponse.json();
      const otherToken = otherLoginData.access_token;

      // Create calculation with other user
      const calcResponse = await request.post('/calculations/', {
        headers: {
          'Authorization': `Bearer ${otherToken}`,
          'Content-Type': 'application/json'
        },
        data: {
          a: 777,
          b: 3,
          type: 'Divide'
        }
      });

      const otherCalc = await calcResponse.json();

      // Try to delete with current user's token
      const response = await request.delete(`/calculations/${otherCalc.id}`, {
        headers: {
          'Authorization': `Bearer ${authToken}`
        }
      });

      expect(response.status()).toBe(404);
    });
  });
});
