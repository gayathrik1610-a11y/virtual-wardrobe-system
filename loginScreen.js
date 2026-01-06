import React, { useState } from 'react';
import { View, Text, TextInput, Button, StyleSheet, Alert, ActivityIndicator } from 'react-native';
import { supabase } from '../supabaseClient';

export default function LoginScreen({ navigation }) {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [loading, setLoading] = useState(false);

  // Validate inputs
  const validateInputs = () => {
    if (!email.includes('@')) {
      Alert.alert('Invalid Email', 'Please enter a valid email address.');
      return false;
    }
    if (password.length < 6) {
      Alert.alert('Invalid Password', 'Password must be at least 6 characters long.');
      return false;
    }
    return true;
  };

  const handleLogin = async () => {
    if (!validateInputs()) return;

    setLoading(true);
    try {
      const { data: { user }, error } = await supabase.auth.signInWithPassword({ email, password });
      if (error) throw error;

      Alert.alert('Success', 'Logged in successfully!');
      // Navigate to Home and you can fetch user-specific outfits there
      navigation.replace('Home', { userEmail: user.email, userId: user.id });
    } catch (error) {
      Alert.alert('Login Error', error.message);
    } finally {
      setLoading(false);
    }
  };

  const handleSignup = async () => {
    if (!validateInputs()) return;

    setLoading(true);
    try {
      const { data, error } = await supabase.auth.signUp({ email, password });
      if (error) throw error;

      Alert.alert(
        'Verify Your Email',
        'A verification link has been sent. Please verify to log in.',
        [{ text: 'OK', onPress: () => navigation.navigate('Login') }]
      );
    } catch (error) {
      Alert.alert('Signup Error', error.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <View style={styles.container}>
      <Text style={styles.title}>Login / Signup</Text>
      <TextInput
        placeholder="Email"
        value={email}
        onChangeText={setEmail}
        style={styles.input}
        keyboardType="email-address"
        autoCapitalize="none"
      />
      <TextInput
        placeholder="Password"
        value={password}
        onChangeText={setPassword}
        style={styles.input}
        secureTextEntry
      />
      {loading ? (
        <ActivityIndicator size="large" color="#0000ff" style={{ marginVertical: 10 }} />
      ) : (
        <>
          <Button title="Login" onPress={handleLogin} />
          <View style={{ height: 10 }} />
          <Button title="Sign Up" onPress={handleSignup} />
        </>
      )}
    </View>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, justifyContent: 'center', padding: 20 },
  title: { fontSize: 22, marginBottom: 20, textAlign: 'center' },
  input: {
    borderWidth: 1,
    borderColor: '#ccc',
    borderRadius: 8,
    padding: 10,
    marginBottom: 15,
  },
});

