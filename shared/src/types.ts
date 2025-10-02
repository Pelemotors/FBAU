import { z } from 'zod';

// Auth Status Types
export const AuthStatusSchema = z.enum(['connected', 'needs_reauth', 'disconnected']);
export type AuthStatus = z.infer<typeof AuthStatusSchema>;

// Post Types
export const PostSchema = z.object({
  id: z.string().uuid(),
  title: z.string().optional(),
  body: z.string().min(1, 'Post body is required'),
  is_ai_generated: z.boolean(),
  media_paths: z.array(z.string()).optional(),
  created_at: z.date(),
  updated_at: z.date(),
});

export type Post = z.infer<typeof PostSchema>;

export const CreatePostSchema = z.object({
  title: z.string().optional(),
  body: z.string().min(1, 'Post body is required'),
  is_ai_generated: z.boolean(),
  media_paths: z.array(z.string()).optional(),
});

export type CreatePost = z.infer<typeof CreatePostSchema>;

// Group Types
export const GroupSchema = z.object({
  id: z.string().uuid(),
  name: z.string().min(1, 'Group name is required'),
  url: z.string().url().refine(url => url.includes('facebook.com'), 'URL must be a Facebook URL'),
  last_status: z.enum(['success', 'failed', 'unknown']).optional(),
  last_checked_at: z.date().optional(),
});

export type Group = z.infer<typeof GroupSchema>;

export const CreateGroupSchema = z.object({
  name: z.string().min(1, 'Group name is required'),
  url: z.string().url().refine(url => url.includes('facebook.com'), 'URL must be a Facebook URL'),
});

export type CreateGroup = z.infer<typeof CreateGroupSchema>;

// Schedule Types
export const ScheduleTypeSchema = z.enum(['one_time', 'recurring']);
export type ScheduleType = z.infer<typeof ScheduleTypeSchema>;

export const ScheduleStatusSchema = z.enum(['pending', 'running', 'done', 'done_with_errors', 'failed', 'paused']);
export type ScheduleStatus = z.infer<typeof ScheduleStatusSchema>;

export const ScheduleSchema = z.object({
  id: z.string().uuid(),
  post_id: z.string().uuid(),
  group_ids: z.array(z.string().uuid()),
  type: ScheduleTypeSchema,
  run_at: z.date().optional(),
  cron: z.string().optional(),
  timezone: z.string().optional(),
  start_at: z.date().optional(),
  end_at: z.date().optional(),
  max_runs: z.number().optional(),
  runs_count: z.number().default(0),
  status: ScheduleStatusSchema,
  last_run_at: z.date().optional(),
  locked_at: z.date().optional(),
  locked_by: z.string().optional(),
  meta_json: z.record(z.any()).optional(),
});

export type Schedule = z.infer<typeof ScheduleSchema>;

export const CreateScheduleSchema = z.object({
  post_id: z.string().uuid(),
  group_ids: z.array(z.string().uuid()),
  type: ScheduleTypeSchema,
  run_at: z.date().optional(),
  cron: z.string().optional(),
  timezone: z.string().optional(),
  start_at: z.date().optional(),
  end_at: z.date().optional(),
  max_runs: z.number().optional(),
});

export type CreateSchedule = z.infer<typeof CreateScheduleSchema>;

// Log Types
export const LogEventSchema = z.enum([
  'publish_attempt',
  'success',
  'fail',
  'auth_issue',
  'ui_changed',
  'rate_limited',
  'duplicate_skipped',
  'worker_start',
  'worker_stop'
]);

export type LogEvent = z.infer<typeof LogEventSchema>;

export const LogSchema = z.object({
  id: z.string().uuid(),
  post_id: z.string().uuid().optional(),
  group_id: z.string().uuid().optional(),
  event: LogEventSchema,
  message: z.string(),
  created_at: z.date(),
  meta_json: z.record(z.any()).optional(),
});

export type Log = z.infer<typeof LogSchema>;

// Connection Types
export const ConnectionSchema = z.object({
  id: z.string().uuid(),
  provider: z.literal('facebook'),
  status: AuthStatusSchema,
  last_verified_at: z.date().optional(),
  notes: z.string().optional(),
});

export type Connection = z.infer<typeof ConnectionSchema>;

// API Response Types
export const ApiResponseSchema = z.object({
  success: z.boolean(),
  data: z.any().optional(),
  error: z.string().optional(),
  message: z.string().optional(),
});

export type ApiResponse<T = any> = {
  success: boolean;
  data?: T;
  error?: string;
  message?: string;
};
