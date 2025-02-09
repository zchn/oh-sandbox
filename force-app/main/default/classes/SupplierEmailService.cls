public class SupplierEmailService {
    public class Supplier {
        public String name;
        public String email;

        public Supplier(String name, String email) {
            this.name = name;
            this.email = email;
        }
    }

    public static void sendEmailToSuppliers(List<Supplier> suppliers, String subject, String emailBody) {
        List<Messaging.SingleEmailMessage> emailMessages = new List<Messaging.SingleEmailMessage>();

        for (Supplier supplier : suppliers) {
            Messaging.SingleEmailMessage email = new Messaging.SingleEmailMessage();
            email.setToAddresses(new String[] { supplier.email });
            email.setSubject(subject);

            String personalizedBody = emailBody.replace('{supplierName}', supplier.name);
            email.setPlainTextBody(personalizedBody);

            emailMessages.add(email);
        }

        if (!emailMessages.isEmpty()) {
            try {
                Messaging.sendEmail(emailMessages);
            } catch (Exception e) {
                System.debug('Error sending emails: ' + e.getMessage());
                throw new SupplierEmailException('Failed to send emails to suppliers: ' + e.getMessage());
            }
        }
    }

    public class SupplierEmailException extends Exception {}
}
