import React, { useState } from 'react';
import { View, Text, TextInput, Button, StyleSheet } from 'react-native';

const UserInputScreen = ({ navigation }) => {
  const [type, setType] = useState('');
  const [color, setColor] = useState('');
  const [event, setEvent] = useState('');

  const handleSubmit = () => {
    if (!type || !color || !event) {
      alert('Please fill in all fields.');
      return;
    }

    navigation.navigate('Recommendation', {
      type: type.toLowerCase(),
      color: color.toLowerCase(),
      event: event.toLowerCase()
    });
  };

  return (
    <View style={styles.container}>
      <Text style={styles.label}>Type (e.g. shirt, dress, pant):</Text>
      <TextInput style={styles.input} value={type} onChangeText={setType} />

      <Text style={styles.label}>Color (e.g. red, black):</Text>
      <TextInput style={styles.input} value={color} onChangeText={setColor} />

      <Text style={styles.label}>Event (e.g. formal, casual, wedding):</Text>
      <TextInput style={styles.input} value={event} onChangeText={setEvent} />

      <Button title="Get Recommendations" onPress={handleSubmit} />
    </View>
  );
};

export default UserInputScreen;

const styles = StyleSheet.create({
  container: { flex: 1, padding: 20 },
  label: { fontSize: 16, marginTop: 20 },
  input: {
    borderWidth: 1,
    borderColor: '#999',
    padding: 10,
    marginTop: 5,
    borderRadius: 5
  }
});
