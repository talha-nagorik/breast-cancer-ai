/**
 * API Helpers - HTTP request utilities and API communication
 */

const api = {
    // Make API request
    request: async function(url, options = {}) {
        const defaultOptions = {
            headers: {
                'Content-Type': 'application/json',
            },
        };

        const config = { ...defaultOptions, ...options };

        try {
            const response = await fetch(url, config);
            const data = await response.json();

            if (!response.ok) {
                throw new Error(data.message || 'An error occurred');
            }

            return data;
        } catch (error) {
            console.error('API request failed:', error);
            throw error;
        }
    },

    // GET request
    get: function(url) {
        return this.request(url, { method: 'GET' });
    },

    // POST request
    post: function(url, data) {
        return this.request(url, {
            method: 'POST',
            body: JSON.stringify(data),
        });
    },

    // PUT request
    put: function(url, data) {
        return this.request(url, {
            method: 'PUT',
            body: JSON.stringify(data),
        });
    },

    // DELETE request
    delete: function(url) {
        return this.request(url, { method: 'DELETE' });
    },

    // Upload file
    uploadFile: async function(url, file, options = {}) {
        const formData = new FormData();
        formData.append('file', file);

        const config = {
            method: 'POST',
            body: formData,
            ...options
        };

        try {
            const response = await fetch(url, config);
            const data = await response.json();

            if (!response.ok) {
                throw new Error(data.message || 'Upload failed');
            }

            return data;
        } catch (error) {
            console.error('File upload failed:', error);
            throw error;
        }
    },

    // Download file
    downloadFile: async function(url, filename) {
        try {
            const response = await fetch(url);
            if (!response.ok) {
                throw new Error('Download failed');
            }

            const blob = await response.blob();
            const downloadUrl = window.URL.createObjectURL(blob);
            const link = document.createElement('a');
            link.href = downloadUrl;
            link.download = filename;
            document.body.appendChild(link);
            link.click();
            document.body.removeChild(link);
            window.URL.revokeObjectURL(downloadUrl);
        } catch (error) {
            console.error('File download failed:', error);
            throw error;
        }
    }
};

// Export for use in other modules
window.BreastCareAI = window.BreastCareAI || {};
window.BreastCareAI.api = api;
