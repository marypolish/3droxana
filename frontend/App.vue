<template>
  <div class="chat-body">
    <nav class="nav-bar">
      <div class="logo">KPI<span>Assistant</span></div>
      <div class="nav-links">
        <router-link to="/">Головна</router-link>
        <router-link to="/chat">Чат</router-link>
        <router-link to="/about">Про</router-link>
        <router-link to="/settings">Налаштування</router-link>
      </div>
    </nav>

    <main class="content-main">
      <router-view></router-view>
    </main>
  </div>
</template>
