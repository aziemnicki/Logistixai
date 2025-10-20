import { createClient } from "@supabase/supabase-js"
import { readFileSync } from "fs"
import { fileURLToPath } from "url"
import { dirname, join } from "path"

const __filename = fileURLToPath(import.meta.url)
const __dirname = dirname(__filename)

// Create Supabase client
const supabase = createClient(
  process.env.SUPABASE_SUPABASE_NEXT_PUBLIC_SUPABASE_URL,
  process.env.SUPABASE_SUPABASE_SERVICE_ROLE_KEY,
)

async function runMigrations() {
  console.log("[v0] Starting database migrations...")

  try {
    // Read and execute each SQL file
    const sqlFiles = ["001_create_tables.sql", "002_seed_reports.sql", "003_seed_interactions.sql"]

    for (const file of sqlFiles) {
      console.log(`[v0] Executing ${file}...`)
      const sql = readFileSync(join(__dirname, file), "utf-8")

      // Split by semicolon and execute each statement
      const statements = sql
        .split(";")
        .map((s) => s.trim())
        .filter((s) => s.length > 0)

      for (const statement of statements) {
        const { error } = await supabase.rpc("exec_sql", { sql_query: statement })
        if (error) {
          console.error(`[v0] Error executing statement:`, error)
          console.error(`[v0] Statement:`, statement.substring(0, 100))
        }
      }

      console.log(`[v0] ✓ ${file} completed`)
    }

    console.log("[v0] All migrations completed successfully!")
  } catch (error) {
    console.error("[v0] Migration error:", error)
  }
}

runMigrations()
