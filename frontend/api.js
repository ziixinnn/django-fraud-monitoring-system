const API = {

    alertList: view => 
        `http://127.0.0.1:8000/alert/get/?view=${view}`,

    alertDetail: alertId =>
        `http://127.0.0.1:8000/alert/get/${alertId}/`,

    alertResolved: alertId =>
        `http://127.0.0.1:8000/alert/get/${alertId}/resolved-detail`,

    alertAnalysis: alertId =>
        `http://127.0.0.1:8000/alert/get/${alertId}/analysis`,

    transactionList: () =>
        `http://127.0.0.1:8000/transaction/get/`,

    transactionDetail: transactionId =>
        `http://127.0.0.1:8000/transaction/get/${transactionId}/`,

    postTransactionAction: transactionId =>
        `http://127.0.0.1:8000/transaction/post/${transactionId}/action/`,

    customerDetail: customerId =>
        `http://127.0.0.1:8000/customer/${customerId}/`,

    customerTransactions: customerId =>
        `http://127.0.0.1:8000/transaction/${customerId}/`,

    customerTransactionsByType: (customerId, type) =>
        `http://127.0.0.1:8000/transaction/${customerId}/?type=${type}`,

    staffLogin: () =>
        `http://127.0.0.1:8000/staff/login/`,

    checkAuth: () =>
        `http://127.0.0.1:8000/staff/auth/check/`
};