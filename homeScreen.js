import React from 'react';
import { View, Text, Button, StyleSheet } from 'react-native';
import { supabase } from '../supabaseClient';

export default function HomeScreen({ navigation }) {
  const handleLogout = async () => {
    await supabase.auth.signOut();
    navigation.replace('Welcome');
  };

  return (
    <View style={styles.container}>
      <Text style={styles.title}>Welcome to your Wardrobe!</Text>
      <Button title="Logout" onPress={handleLogout} />
    </View>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, justifyContent: 'center', alignItems: 'center', padding: 20 },
  title: { fontSize: 24, marginBottom: 20, textAlign: 'center' },
});