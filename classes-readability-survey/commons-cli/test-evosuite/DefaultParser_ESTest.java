/*
 * This file was automatically generated by EvoSuite
 * Tue Apr 30 11:41:02 GMT 2024
 */

package org.apache.commons.cli;

import org.junit.Test;
import static org.junit.Assert.*;
import static org.evosuite.runtime.EvoAssertions.*;
import java.util.Properties;
import java.util.function.Consumer;
import org.apache.commons.cli.CommandLine;
import org.apache.commons.cli.DefaultParser;
import org.apache.commons.cli.Option;
import org.apache.commons.cli.OptionGroup;
import org.apache.commons.cli.Options;
import org.evosuite.runtime.EvoRunner;
import org.evosuite.runtime.EvoRunnerParameters;
import org.junit.runner.RunWith;

public class DefaultParser_ESTest {

  @Test(timeout = 4000)
  public void test00()  throws Throwable  {
      DefaultParser defaultParser0 = new DefaultParser(false);
      Options options0 = new Options();
      String[] stringArray0 = new String[7];
      stringArray0[0] = "org.apache.commons.cli.DefaultParser$1";
      Properties properties0 = new Properties();
      defaultParser0.parse(options0, stringArray0, properties0, true);
      defaultParser0.handleConcatenatedOptions("zN*-RY*%'OO=Z/iNL");
  }

  @Test(timeout = 4000)
  public void test01()  throws Throwable  {
      DefaultParser defaultParser0 = new DefaultParser(false);
      defaultParser0.handleConcatenatedOptions("");
  }

  @Test(timeout = 4000)
  public void test02()  throws Throwable  {
      DefaultParser defaultParser0 = new DefaultParser(false);
      Options options0 = new Options();
      String[] stringArray0 = new String[7];
      stringArray0[0] = "0_v";
      stringArray0[1] = "]u%2<O:4cq%GW)r";
      stringArray0[2] = "[";
      stringArray0[3] = "Unrecognized option: ";
      stringArray0[4] = "Io7~Cz_|mnP(Eq#";
      stringArray0[5] = "-";
      stringArray0[6] = "-org.apache.commons.cli.Option$1";
      Properties properties0 = new Properties();
      try { 
        defaultParser0.parse(options0, stringArray0, properties0);
        fail("Expecting exception: Exception");
      
      } catch(Exception e) {
         //
         // Unrecognized option: -org.apache.commons.cli.Option$1
         //
         verifyException("org.apache.commons.cli.DefaultParser", e);
      }
  }

  @Test(timeout = 4000)
  public void test03()  throws Throwable  {
      DefaultParser defaultParser0 = new DefaultParser();
      Options options0 = new Options();
      String[] stringArray0 = new String[4];
      stringArray0[0] = "q)3_zU";
      stringArray0[1] = "HLmj9RJJB;3_]$Ek^o";
      stringArray0[2] = "";
      stringArray0[3] = "l";
      Properties properties0 = new Properties();
      defaultParser0.parse(options0, stringArray0, properties0);
      defaultParser0.checkRequiredOptions();
  }

  @Test(timeout = 4000)
  public void test04()  throws Throwable  {
      DefaultParser defaultParser0 = new DefaultParser();
      Options options0 = new Options();
      String[] stringArray0 = new String[6];
      stringArray0[0] = "--7+JB5\"3g3&+ H}ZM@Z";
      CommandLine commandLine0 = defaultParser0.parse(options0, stringArray0, true);
      assertNotNull(commandLine0);
  }

  @Test(timeout = 4000)
  public void test05()  throws Throwable  {
      DefaultParser defaultParser0 = new DefaultParser();
      Options options0 = new Options();
      Properties properties0 = new Properties();
      CommandLine commandLine0 = defaultParser0.parse(options0, (String[]) null, properties0);
      assertNotNull(commandLine0);
  }

  @Test(timeout = 4000)
  public void test06()  throws Throwable  {
      DefaultParser defaultParser0 = new DefaultParser();
      Options options0 = new Options();
      String[] stringArray0 = new String[2];
      stringArray0[0] = "3GEzXoL5X C";
      stringArray0[1] = "";
      CommandLine commandLine0 = defaultParser0.parse(options0, stringArray0);
      assertNotNull(commandLine0);
  }

  @Test(timeout = 4000)
  public void test07()  throws Throwable  {
      DefaultParser.Builder defaultParser_Builder0 = DefaultParser.builder();
      DefaultParser defaultParser0 = defaultParser_Builder0.build();
      Options options0 = new Options();
      String[] stringArray0 = new String[4];
      stringArray0[0] = "";
      stringArray0[1] = "7i|Qs<x+]-V%";
      stringArray0[2] = "org.apache.commons.cli.CommandLine$1";
      stringArray0[3] = "m94";
      Properties properties0 = new Properties();
      OptionGroup optionGroup0 = new OptionGroup();
      Object object0 = new Object();
      properties0.put(optionGroup0, object0);
      // Undeclared exception!
      try { 
        defaultParser0.parse(options0, stringArray0, properties0, false);
        fail("Expecting exception: ClassCastException");
      
      } catch(ClassCastException e) {
         //
         // org.apache.commons.cli.OptionGroup cannot be cast to java.lang.String
         //
         verifyException("java.util.Properties", e);
      }
  }

  @Test(timeout = 4000)
  public void test08()  throws Throwable  {
      DefaultParser defaultParser0 = new DefaultParser();
      String[] stringArray0 = new String[5];
      Properties properties0 = new Properties();
      // Undeclared exception!
      try { 
        defaultParser0.parse((Options) null, stringArray0, properties0);
        fail("Expecting exception: NullPointerException");
      
      } catch(NullPointerException e) {
         //
         // no message in exception (getMessage() returned null)
         //
         verifyException("org.apache.commons.cli.DefaultParser", e);
      }
  }

  @Test(timeout = 4000)
  public void test09()  throws Throwable  {
      DefaultParser.Builder defaultParser_Builder0 = DefaultParser.builder();
      DefaultParser defaultParser0 = defaultParser_Builder0.build();
      Options options0 = new Options();
      Properties properties0 = new Properties();
      Object object0 = new Object();
      properties0.put(object0, defaultParser_Builder0);
      // Undeclared exception!
      try { 
        defaultParser0.parse(options0, (String[]) null, properties0);
        fail("Expecting exception: ClassCastException");
      
      } catch(ClassCastException e) {
         //
         // java.lang.Object cannot be cast to java.lang.String
         //
         verifyException("java.util.Properties", e);
      }
  }

  @Test(timeout = 4000)
  public void test10()  throws Throwable  {
      DefaultParser defaultParser0 = new DefaultParser(false);
      // Undeclared exception!
      try { 
        defaultParser0.handleConcatenatedOptions("#j9m,iAye>[q^r)xxB.");
        fail("Expecting exception: NullPointerException");
      
      } catch(NullPointerException e) {
         //
         // no message in exception (getMessage() returned null)
         //
         verifyException("org.apache.commons.cli.DefaultParser", e);
      }
  }

  @Test(timeout = 4000)
  public void test11()  throws Throwable  {
      DefaultParser defaultParser0 = new DefaultParser();
      // Undeclared exception!
      try { 
        defaultParser0.checkRequiredOptions();
        fail("Expecting exception: NullPointerException");
      
      } catch(NullPointerException e) {
      }
  }

  @Test(timeout = 4000)
  public void test12()  throws Throwable  {
      DefaultParser.Builder defaultParser_Builder0 = DefaultParser.builder();
      DefaultParser defaultParser0 = defaultParser_Builder0.build();
      Options options0 = new Options();
      OptionGroup optionGroup0 = new OptionGroup();
      Option option0 = new Option((String) null, "1Q:EEH5+'m{~=]r[#f", true, "A");
      OptionGroup optionGroup1 = optionGroup0.addOption(option0);
      options0.addOptionGroup(optionGroup1);
      String[] stringArray0 = new String[4];
      // Undeclared exception!
      try { 
        defaultParser0.parse(options0, stringArray0, (Properties) null, true);
        fail("Expecting exception: NullPointerException");
      
      } catch(NullPointerException e) {
      }
  }

  @Test(timeout = 4000)
  public void test13()  throws Throwable  {
      DefaultParser.Builder defaultParser_Builder0 = DefaultParser.builder();
      DefaultParser defaultParser0 = defaultParser_Builder0.build();
      Options options0 = new Options();
      OptionGroup optionGroup0 = new OptionGroup();
      Option option0 = new Option((String) null, "1Q:EEH5+'m{~=]r[#f", true, "A");
      OptionGroup optionGroup1 = optionGroup0.addOption(option0);
      options0.addOptionGroup(optionGroup1);
      String[] stringArray0 = new String[4];
      // Undeclared exception!
      try { 
        defaultParser0.parse(options0, stringArray0, false);
        fail("Expecting exception: NullPointerException");
      
      } catch(NullPointerException e) {
      }
  }

  @Test(timeout = 4000)
  public void test14()  throws Throwable  {
      DefaultParser.Builder defaultParser_Builder0 = DefaultParser.builder();
      DefaultParser defaultParser0 = defaultParser_Builder0.build();
      Options options0 = new Options();
      String[] stringArray0 = new String[6];
      stringArray0[0] = "--";
      Properties properties0 = new Properties();
      CommandLine commandLine0 = defaultParser0.parse(options0, stringArray0, properties0, false);
      assertNotNull(commandLine0);
  }

  @Test(timeout = 4000)
  public void test15()  throws Throwable  {
      DefaultParser defaultParser0 = new DefaultParser(false);
      Options options0 = new Options();
      String[] stringArray0 = new String[7];
      stringArray0[0] = "-/";
      Properties properties0 = new Properties();
      try { 
        defaultParser0.parse(options0, stringArray0, properties0, false);
        fail("Expecting exception: Exception");
      
      } catch(Exception e) {
         //
         // Unrecognized option: -/
         //
         verifyException("org.apache.commons.cli.DefaultParser", e);
      }
  }

  @Test(timeout = 4000)
  public void test16()  throws Throwable  {
      DefaultParser defaultParser0 = new DefaultParser();
      Options options0 = new Options();
      String[] stringArray0 = new String[8];
      stringArray0[0] = "-=6#l";
      Properties properties0 = new Properties();
      properties0.put("-=6#l", "c");
      try { 
        defaultParser0.parse(options0, stringArray0, properties0, true);
        fail("Expecting exception: Exception");
      
      } catch(Exception e) {
         //
         // Default option wasn't defined
         //
         verifyException("org.apache.commons.cli.DefaultParser", e);
      }
  }

  @Test(timeout = 4000)
  public void test17()  throws Throwable  {
      DefaultParser defaultParser0 = new DefaultParser();
      Options options0 = new Options();
      String[] stringArray0 = new String[9];
      stringArray0[0] = "1Q:EEH5+'m{~=]r[#f";
      stringArray0[1] = "";
      stringArray0[2] = "liCfeedFjZ";
      stringArray0[3] = "aKG'9 PL(AC0h";
      stringArray0[4] = "--1Q:EEH5+'m{~=]r[#f";
      try { 
        defaultParser0.parse(options0, stringArray0);
        fail("Expecting exception: Exception");
      
      } catch(Exception e) {
         //
         // Unrecognized option: --1Q:EEH5+'m{~=]r[#f
         //
         verifyException("org.apache.commons.cli.DefaultParser", e);
      }
  }

  @Test(timeout = 4000)
  public void test18()  throws Throwable  {
      DefaultParser.Builder defaultParser_Builder0 = DefaultParser.builder();
      DefaultParser defaultParser0 = defaultParser_Builder0.build();
      Options options0 = new Options();
      String[] stringArray0 = new String[8];
      stringArray0[0] = "M:J[9E";
      stringArray0[1] = "-";
      stringArray0[2] = "-";
      stringArray0[3] = "-";
      stringArray0[4] = "-";
      stringArray0[5] = "j'xl?kB>N<*tULG";
      stringArray0[6] = "-";
      stringArray0[7] = "-";
      Properties properties0 = new Properties();
      defaultParser0.parse(options0, stringArray0, properties0, false);
      try { 
        defaultParser0.handleConcatenatedOptions("--true");
        fail("Expecting exception: Exception");
      
      } catch(Exception e) {
         //
         // Unrecognized option: --true
         //
         verifyException("org.apache.commons.cli.DefaultParser", e);
      }
  }

  @Test(timeout = 4000)
  public void test19()  throws Throwable  {
      DefaultParser.Builder defaultParser_Builder0 = DefaultParser.builder();
      DefaultParser defaultParser0 = defaultParser_Builder0.build();
      defaultParser0.handleConcatenatedOptions("<");
  }

  @Test(timeout = 4000)
  public void test20()  throws Throwable  {
      DefaultParser defaultParser0 = new DefaultParser(false);
      Options options0 = new Options();
      String[] stringArray0 = new String[4];
      stringArray0[0] = "vE7LTc;^A%";
      stringArray0[1] = "vE7LTc;^A%";
      stringArray0[2] = "--org.apache.commons.cli.HelpFormatter$Builder";
      try { 
        defaultParser0.parse(options0, stringArray0, false);
        fail("Expecting exception: Exception");
      
      } catch(Exception e) {
         //
         // Unrecognized option: --org.apache.commons.cli.HelpFormatter$Builder
         //
         verifyException("org.apache.commons.cli.DefaultParser", e);
      }
  }

  @Test(timeout = 4000)
  public void test21()  throws Throwable  {
      DefaultParser defaultParser0 = new DefaultParser();
      Options options0 = new Options();
      String[] stringArray0 = new String[6];
      stringArray0[0] = "-org.apache.commons.cli.HelpFormatter$Builder";
      CommandLine commandLine0 = defaultParser0.parse(options0, stringArray0, true);
      assertNotNull(commandLine0);
  }

  @Test(timeout = 4000)
  public void test22()  throws Throwable  {
      DefaultParser.Builder defaultParser_Builder0 = DefaultParser.builder();
      DefaultParser defaultParser0 = defaultParser_Builder0.build();
      Options options0 = new Options();
      String[] stringArray0 = new String[5];
      stringArray0[0] = "-";
      options0.addRequiredOption((String) null, "", true, "true");
      try { 
        defaultParser0.parse(options0, stringArray0, true);
        fail("Expecting exception: Exception");
      
      } catch(Exception e) {
         //
         // Missing required option: 
         //
         verifyException("org.apache.commons.cli.DefaultParser", e);
      }
  }

  @Test(timeout = 4000)
  public void test23()  throws Throwable  {
      DefaultParser.Builder defaultParser_Builder0 = DefaultParser.builder();
      Boolean boolean0 = Boolean.FALSE;
      DefaultParser defaultParser0 = defaultParser_Builder0.build();
      Options options0 = new Options();
      Properties properties0 = new Properties();
      CommandLine commandLine0 = defaultParser0.parse(options0, (String[]) null, properties0, (boolean) boolean0);
      assertNotNull(commandLine0);
  }

  @Test(timeout = 4000)
  public void test24()  throws Throwable  {
      DefaultParser defaultParser0 = new DefaultParser();
      Options options0 = new Options();
      String[] stringArray0 = new String[9];
      // Undeclared exception!
      try { 
        defaultParser0.parse(options0, stringArray0);
        fail("Expecting exception: NullPointerException");
      
      } catch(NullPointerException e) {
      }
  }

  @Test(timeout = 4000)
  public void test25()  throws Throwable  {
      DefaultParser defaultParser0 = new DefaultParser(true);
      Options options0 = new Options();
      String[] stringArray0 = new String[3];
      stringArray0[0] = "GI;";
      stringArray0[1] = "Default option wasn't defined";
      stringArray0[2] = "-w=`LP^Q**n0u;";
      Properties properties0 = new Properties();
      try { 
        defaultParser0.parse(options0, stringArray0, properties0);
        fail("Expecting exception: Exception");
      
      } catch(Exception e) {
         //
         // Unrecognized option: -w=`LP^Q**n0u;
         //
         verifyException("org.apache.commons.cli.DefaultParser", e);
      }
  }

  @Test(timeout = 4000)
  public void test26()  throws Throwable  {
      DefaultParser.Builder defaultParser_Builder0 = DefaultParser.builder();
      DefaultParser.Builder defaultParser_Builder1 = defaultParser_Builder0.setAllowPartialMatching(true);
      assertSame(defaultParser_Builder1, defaultParser_Builder0);
  }

  @Test(timeout = 4000)
  public void test27()  throws Throwable  {
      DefaultParser.Builder defaultParser_Builder0 = DefaultParser.builder();
      DefaultParser.Builder defaultParser_Builder1 = defaultParser_Builder0.setDeprecatedHandler((Consumer<Option>) null);
      assertSame(defaultParser_Builder1, defaultParser_Builder0);
  }

  @Test(timeout = 4000)
  public void test28()  throws Throwable  {
      DefaultParser.Builder defaultParser_Builder0 = DefaultParser.builder();
      Boolean boolean0 = Boolean.valueOf("-");
      DefaultParser.Builder defaultParser_Builder1 = defaultParser_Builder0.setStripLeadingAndTrailingQuotes(boolean0);
      assertSame(defaultParser_Builder0, defaultParser_Builder1);
  }
}
