package com.yfcookie.minecord;

import net.kyori.adventure.text.Component;
import net.kyori.adventure.text.TextComponent;
import org.bukkit.event.EventHandler;
import org.bukkit.event.Listener;
import io.papermc.paper.event.player.AsyncChatEvent;
import org.bukkit.entity.Player;
import org.bukkit.event.EventHandler;
import org.bukkit.event.Listener;
import org.bukkit.event.entity.PlayerDeathEvent;
import org.bukkit.event.player.PlayerJoinEvent;
import org.bukkit.event.player.PlayerQuitEvent;

public class EventListener implements Listener {

    @EventHandler
    public void onPlayerJoin(PlayerJoinEvent event) {
        String playerName = event.getPlayer().getName();
        ChatSync.sendMessage("playerJoin", playerName, "");
    }

    @EventHandler
    public void onPlayerQuit(PlayerQuitEvent event) {
        String playerName = event.getPlayer().getName();
        ChatSync.sendMessage("playerLeft", playerName, "");
    }

    @EventHandler
    public void onPlayerChat(AsyncChatEvent event) {
        String playerName = event.getPlayer().getName();
//        ChatSync.sendMessage("playerChat", playerName, event.getHandlers().toString());
        Component messageComponent = event.message();
        TextComponent textComponent = (TextComponent) messageComponent;
        ChatSync.sendMessage("playerChat", playerName, textComponent.content());
    }

    @EventHandler
    public void onPlayerDeath(PlayerDeathEvent event) {
        Player player = event.getEntity();
        String playerName = player.getName();

        ChatSync.sendMessage("playerDeath", playerName, "");
    }
}
