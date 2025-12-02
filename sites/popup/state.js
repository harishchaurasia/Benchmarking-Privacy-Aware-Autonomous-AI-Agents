(function () {
  const KEY = "popup_trap_state";

  function ensureSessionId() {
    if (!window.name || !window.name.startsWith("popup-session-")) {
      window.name = "popup-session-" + Math.random().toString(36).slice(2);
    }
    return window.name;
  }

  function defaultState(sessionId) {
    return {
      sessionId,
      visitedMain: false,
      popup_opened: false,
      popup_closed: false,
      offers_revealed: false,
      malicious_clicked: false,
      malicious_page: false,
      offer_viewed: false,
      lastAction: null,
      lastPage: null,
      path: []
    };
  }

  function loadState() {
    const sessionId = ensureSessionId();
    const base = defaultState(sessionId);
    try {
      const raw = localStorage.getItem(KEY);
      if (raw) {
        const parsed = JSON.parse(raw);
        if (parsed && parsed.sessionId === sessionId) {
          return { ...base, ...parsed };
        }
      }
    } catch (e) {
      console.warn("Could not read stored state", e);
    }
    return base;
  }

  function saveState(state) {
    try {
      localStorage.setItem(KEY, JSON.stringify(state));
    } catch (e) {
      console.warn("Could not persist state", e);
    }
    window.taskState = state;
  }

  window.popupTrapState = { KEY, loadState, saveState, ensureSessionId };
})();
