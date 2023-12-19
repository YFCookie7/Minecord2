package com.yfcookie.minecord;

import org.bukkit.plugin.java.JavaPlugin;

public final class Minecord extends JavaPlugin {
    private ChatSync ChatSync;

    @Override
    public void onEnable() {
        getServer().getPluginManager().registerEvents(new EventListener(), this);
        ChatSync = new ChatSync();
        com.yfcookie.minecord.ChatSync.sendMessage("serverStart", "", "");
    }

    @Override
    public void onDisable() {
        com.yfcookie.minecord.ChatSync.sendMessage("serverStop", "", "");
    }
}
