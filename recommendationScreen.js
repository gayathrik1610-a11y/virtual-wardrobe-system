import React, { useEffect, useState } from 'react';
import { View, Text, ActivityIndicator, ScrollView, StyleSheet, Image } from 'react-native';
import { createClient } from '@supabase/supabase-js';


const supabaseUrl = 'https://lhjvaivpaxuaqabkrgst.supabase.co';
const supabaseKey = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImxoanZhaXZwYXh1YXFhYmtyZ3N0Iiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc1NTQ3MDIzMywiZXhwIjoyMDcxMDQ2MjMzfQ.oJtb_ZkO1sPOeVHoRQgqtcOes6Eae-WRPiOEvtrNZjI';
SUPABASE_TABLE_NAME='Outfits';
const supabase = createClient(supabaseUrl, supabaseKey);

const RecommendationScreen = ({ route }) => {
  const { type, color, event } = route.params;
  const [recommendations, setRecommendations] = useState([]);
  const [loading, setLoading] = useState(true);

  const getRecommendationTypes = (inputType) => {
    const accessories = ['shoes', 'belt', 'chain', 'watch'];
    if (inputType === 'shirt') {
      return ['pant', ...accessories];
    } else if (inputType === 'pant') {
      return ['shirt', ...accessories];
    } else if (inputType === 'dress') {
      return ['pant', ...accessories];
    } else {
      return accessories;
    }
  };

  const filteredTypes = getRecommendationTypes(type);

  useEffect(() => {
    const fetchRecommendations = async () => {
      try {
        const { data, error } = await supabase
          .from('Outfits') 
          .select('*')
          .in('type', filteredTypes)
          .eq('event', event)
          .eq('color', color); // Include color match

        if (error) {
          console.error('Supabase error:', error.message);
        } else {
          setRecommendations(data);
        }
      } catch (err) {
        console.error('Unexpected error:', err);
      } finally {
        setLoading(false);
      }
    };

    fetchRecommendations();
  }, [type, color, event]);

  if (loading) {
    return <ActivityIndicator size="large" style={{ marginTop: 50 }} />;
  }

  return (
    <ScrollView contentContainerStyle={styles.container}>
      <Text style={styles.title}>
        Based on your {type} ({color}, {event}), here are matching items:
      </Text>

      {recommendations.length === 0 ? (
        <Text style={styles.noData}>No matching items found for this combination.</Text>
      ) : (
        recommendations.map((item, index) => (
          <View key={index} style={styles.card}>
            <Text style={styles.itemType}>{item.type.toUpperCase()}</Text>
            <Text>Color: {item.color}</Text>
            <Text>Event: {item.event}</Text>
            {item.image_url ? (
              <Image source={{ uri: item.image_url }} style={styles.image} />
            ) : (
              <Text>No image available</Text>
            )}
          </View>
        ))
      )}
    </ScrollView>
  );
};

export default RecommendationScreen;

const styles = StyleSheet.create({
  container: { padding: 20 },
  title: { fontSize: 20, fontWeight: 'bold', marginBottom: 20 },
  noData: { fontSize: 16, color: 'gray', textAlign: 'center' },
  card: {
    padding: 15,
    borderWidth: 1,
    borderColor: '#ccc',
    borderRadius: 8,
    marginBottom: 15,
    backgroundColor: '#f9f9f9'
  },
  itemType: { fontWeight: 'bold', fontSize: 16, marginBottom: 5 },
  image: {
    width: '100%',
    height: 150,
    resizeMode: 'cover',
    marginTop: 10,
    borderRadius: 6
  }
});