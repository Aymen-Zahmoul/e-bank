/**
 * Transaction Service
 * Handles fetching and creating transactions
 */
export const transactionService = {
    getRecentTransactions: async () => {
        // Mock data
        return [
            { id: 1, name: 'Apple Store Monthly', date: 'Sept 12, 2024', amount: -14.99, status: 'Completed', category: 'Technology' },
            { id: 2, name: 'Vanguard Dividend', date: 'Sept 10, 2024', amount: 1240.50, status: 'Completed', category: 'Investment' },
            { id: 3, name: 'Starbucks Coffee', date: 'Sept 09, 2024', amount: -5.50, status: 'Completed', category: 'Food' }
        ];
    },
    getAllTransactions: async () => {
        // Mock data
        return [
            { id: 1, name: 'Amazon Web Services', date: 'Sept 14, 2024', amount: -1240.00, status: 'Success', category: 'Technology' },
            { id: 2, name: 'Dividend Payout', date: 'Sept 13, 2024', amount: 450.25, status: 'Success', category: 'Investment' },
            { id: 3, name: 'Uber Trip', date: 'Sept 13, 2024', amount: -24.50, status: 'Success', category: 'Transport' }
        ];
    }
};
