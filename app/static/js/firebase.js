/**
 * FirebaseController - A modular Firebase controller for web applications
 * @version 1.0.0
 * @license MIT
 */

const FirebaseController = (() => {
    // Default configuration
    let config = null;
    let app = null;
    let auth = null;
    let database = null;
    let listeners = new Map();
    let authStateListeners = [];
    let currentUser = null;

    // Initialize Firebase with configuration
    const initialize = async (firebaseConfig) => {
        if (app) {
            console.warn('Firebase is already initialized');
            return app;
        }

        try {
            // Import Firebase modules dynamically
            const { initializeApp } = await import('https://www.gstatic.com/firebasejs/12.1.0/firebase-app.js');
            const { getAuth, onAuthStateChanged } = await import('https://www.gstatic.com/firebasejs/12.1.0/firebase-auth.js');
            const { getDatabase, ref, onValue, off, set, update, remove } = await import('https://www.gstatic.com/firebasejs/12.1.0/firebase-database.js');
            
            // Store references to Firebase functions
            FirebaseController._firebase = { ref, onValue, off, set, update, remove };
            
            // Initialize Firebase
            config = firebaseConfig;
            app = initializeApp(firebaseConfig);
            auth = getAuth(app);
            database = getDatabase(app);
            
            // Set up auth state listener
            onAuthStateChanged(auth, (user) => {
                currentUser = user;
                authStateListeners.forEach(listener => listener(user));
            });
            
            return app;
        } catch (error) {
            console.error('Failed to initialize Firebase:', error);
            throw error;
        }
    };

    // Listen to auth state changes
    const onAuthStateChange = (callback) => {
        if (typeof callback !== 'function') return () => {};
        
        authStateListeners.push(callback);
        if (currentUser) {
            callback(currentUser);
        }
        
        // Return unsubscribe function
        return () => {
            authStateListeners = authStateListeners.filter(cb => cb !== callback);
        };
    };

    // Get current user
    const getCurrentUser = () => {
        return currentUser;
    };

    // Listen to database changes
    const listen = (path, callback, options = {}) => {
        if (!app) {
            console.error('Firebase not initialized. Call initialize() first.');
            return () => {};
        }

        const { once = false, onlyNew = false } = options;
        const { ref, onValue, off } = FirebaseController._firebase;
        
        const dbRef = ref(database, path);
        let firstCall = true;
        
        const handleValue = (snapshot) => {
            if (onlyNew && firstCall) {
                firstCall = false;
                return;
            }
            
            const value = snapshot.val();
            callback(value, snapshot);
            
            if (once) {
                off(dbRef);
                listeners.delete(path);
            }
        };
        
        // Remove any existing listener for this path
        const unsubscribe = listeners.get(path);
        if (unsubscribe) {
            unsubscribe();
        }
        
        // Set up new listener
        onValue(dbRef, handleValue);
        
        // Store unsubscribe function
        const newUnsubscribe = () => {
            off(dbRef);
            listeners.delete(path);
        };
        
        listeners.set(path, newUnsubscribe);
        return newUnsubscribe;
    };

    // Set data at a specific path
    const setData = async (path, data) => {
        if (!app) {
            throw new Error('Firebase not initialized. Call initialize() first.');
        }
        
        const { ref, set } = FirebaseController._firebase;
        const dbRef = ref(database, path);
        
        try {
            await set(dbRef, data);
            return true;
        } catch (error) {
            console.error('Error setting data:', error);
            throw error;
        }
    };

    // Update data at a specific path
    const updateData = async (path, updates) => {
        if (!app) {
            throw new Error('Firebase not initialized. Call initialize() first.');
        }
        
        const { ref, update } = FirebaseController._firebase;
        const dbRef = ref(database, path);
        
        try {
            await update(dbRef, updates);
            return true;
        } catch (error) {
            console.error('Error updating data:', error);
            throw error;
        }
    };

    // Remove data at a specific path
    const removeData = async (path) => {
        if (!app) {
            throw new Error('Firebase not initialized. Call initialize() first.');
        }
        
        const { ref, remove } = FirebaseController._firebase;
        const dbRef = ref(database, path);
        
        try {
            await remove(dbRef);
            return true;
        } catch (error) {
            console.error('Error removing data:', error);
            throw error;
        }
    };

    // Get data once (without setting up a listener)
    const getDataOnce = async (path) => {
        if (!app) {
            throw new Error('Firebase not initialized. Call initialize() first.');
        }
        
        const { ref, get } = FirebaseController._firebase;
        const dbRef = ref(database, path);
        
        try {
            const snapshot = await get(dbRef);
            return snapshot.val();
        } catch (error) {
            console.error('Error getting data:', error);
            throw error;
        }
    };

    // Clean up all listeners
    const cleanup = () => {
        listeners.forEach(unsubscribe => unsubscribe());
        listeners.clear();
        authStateListeners = [];
    };

    // Public API
    return {
        // Core methods
        initialize,
        cleanup,
        
        // Auth methods
        onAuthStateChange,
        getCurrentUser,
        
        // Database methods
        listen,
        set: setData,
        update: updateData,
        remove: removeData,
        getOnce: getDataOnce,
        
        // Access to Firebase instances (for advanced usage)
        getApp: () => app,
        getAuth: () => auth,
        getDatabase: () => database
    };
})();

// Export for different module systems
if (typeof module !== 'undefined' && typeof module.exports !== 'undefined') {
    module.exports = FirebaseController;
} else if (typeof define === 'function' && define.amd) {
    define([], () => FirebaseController);
} else {
    window.FirebaseController = FirebaseController;
}