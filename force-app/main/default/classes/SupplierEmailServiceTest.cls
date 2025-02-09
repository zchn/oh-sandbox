@isTest
private class SupplierEmailServiceTest {
    @isTest
    static void testSendEmailToSuppliers() {
        // Create test suppliers
        List<SupplierEmailService.Supplier> suppliers = new List<SupplierEmailService.Supplier>();
        suppliers.add(new SupplierEmailService.Supplier('Test Supplier 1', 'supplier1@test.com'));
        suppliers.add(new SupplierEmailService.Supplier('Test Supplier 2', 'supplier2@test.com'));

        String subject = 'Test Email Subject';
        String emailBody = 'Hello {supplierName}, this is a test email.';

        Test.startTest();

        // Verify no exception is thrown when sending emails
        try {
            SupplierEmailService.sendEmailToSuppliers(suppliers, subject, emailBody);

            // Verify that the correct number of emails were sent
            Integer emailInvocations = Limits.getEmailInvocations();
            System.assertEquals(1, emailInvocations, 'Expected one email invocation');

        } catch (Exception e) {
            System.assert(false, 'No exception should be thrown: ' + e.getMessage());
        }

        Test.stopTest();
    }

    @isTest
    static void testSendEmailToEmptySupplierList() {
        List<SupplierEmailService.Supplier> suppliers = new List<SupplierEmailService.Supplier>();
        String subject = 'Test Subject';
        String emailBody = 'Test Body';

        Test.startTest();

        // Verify no exception is thrown with empty supplier list
        try {
            SupplierEmailService.sendEmailToSuppliers(suppliers, subject, emailBody);
            Integer emailInvocations = Limits.getEmailInvocations();
            System.assertEquals(0, emailInvocations, 'No emails should be sent for empty supplier list');
        } catch (Exception e) {
            System.assert(false, 'No exception should be thrown: ' + e.getMessage());
        }

        Test.stopTest();
    }
}
