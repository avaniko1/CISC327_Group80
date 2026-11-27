import { test, expect } from '@playwright/test';
test('Rent Equipment', async ({ page }) => {
    await page.goto('http://127.0.0.1:5000/');

    const rentals = page.getByRole('link', { name: 'Rentals' });
    const renters = page.getByRole('link', { name: 'Renters' });
    const equipment = page.getByRole('link', { name: 'Equipment' });

    await renters.click();
    await page.getByLabel('Name').fill('James Parker');
    await page.getByLabel('Email').fill('j.parker@gmail.com');
    await page.getByRole('button', { name: 'Add Renter' }).click();

    await equipment.click();

    await page.getByLabel('Name').fill('Kayak');
    await page.getByLabel('Category').fill('Boats');
    await page.getByLabel('Total Units').fill('15');
    await page.getByRole('button', { name: 'Add Equipment' }).click();

    await rentals.click();

    await page.getByLabel('Equipment ID').fill('1');
    await page.getByLabel('Renter ID').fill('1');
    await page.getByRole('button', { name: 'Check Out' }).click();

    const rental_list = page.getByRole('list', { name: 'Rentals' });
    await expect(page.getByText('1')).toBeVisible();
});

test('Rent non-ex Equipment', async ({ page }) => {
    await page.goto('http://127.0.0.1:5000/');

    const rentals = page.getByRole('link', { name: 'Rentals' });
    const renters = page.getByRole('link', { name: 'Renters' });

    await renters.click();
    await page.getByLabel('Name').fill('James Parker');
    await page.getByLabel('Email').fill('j.parker@gmail.com');
    await page.getByRole('button', { name: 'Add Renter' }).click();

    await rentals.click();

    await page.getByLabel('Equipment ID').fill('1');
    await page.getByLabel('Renter ID').fill('1');
    await page.getByRole('button', { name: 'Check Out' }).click();

    const rental_list = page.getByRole('list', { name: 'Rentals' });
    await expect(page.getByText('1')).toBeVisible();
});