<template>
    <div class="container">
      <img src="/public/img/index-logo.png" alt="Logo" class="index-logo" />
  
      <!-- Software-Gruppe -->
      <div class="group">
        <span class="group-title">Software</span>
        <div class="button-container">
          <button id="btnDatabaseReset">
            <span class="material-icons icon-button">history</span>Datenbank zurücksetzen
          </button>
          <button id="btnUpdateSoftware">
            <span class="material-icons icon-button">upgrade</span>Aktualisierung durchführen
          </button>
        </div>
      </div>
  
      <!-- Protokoll-Gruppe -->
      <div class="group">
        <span class="group-title">Protokoll</span>
        <div class="button-container">
          <button id="btnAddNote">
            <span class="material-icons icon-button">edit_note</span>Eintrag hinzufügen
          </button>
        </div>
      </div>
  
      <!-- System-Gruppe -->
      <div class="group">
        <span class="group-title">System</span>
        <div class="button-container">
          <button id="btnReboot">
            <span class="material-icons icon-button">restart_alt</span>Hardware neustarten
          </button>
          <button id="btnShutdown">
            <span class="material-icons icon-button">power_settings_new</span>Sicher herunterfahren
          </button>
        </div>
      </div>
  
      <!-- Logout -->
      <button id="logoutButton" class="button-logout">
        <span class="material-icons icon-button">logout</span>Abmelden
      </button>
    </div>
  </template>
  
  <script setup>
  // Die Logik (z. B. modal.show... / fetch...) folgt im nächsten Schritt
  </script>
  