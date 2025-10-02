import dotenv from 'dotenv';
import cron from 'node-cron';

// Load environment variables
dotenv.config();

console.log('🚀 Worker started');
console.log('⏰ Timezone:', process.env.SCHED_TIMEZONE || 'Asia/Jerusalem');
console.log('🔄 Poll interval:', process.env.SCHED_POLL_INTERVAL_MS || '30000ms');

// Basic heartbeat every 30 seconds
cron.schedule('*/30 * * * * *', () => {
  console.log(`💓 Worker heartbeat: ${new Date().toISOString()}`);
});

// This will be expanded later with actual scheduling logic
console.log('📋 Worker is ready to process scheduled tasks');
console.log('🔗 Will connect to server API for task management');

// Keep the process running
process.on('SIGINT', () => {
  console.log('🛑 Worker shutting down...');
  process.exit(0);
});

process.on('SIGTERM', () => {
  console.log('🛑 Worker shutting down...');
  process.exit(0);
});
